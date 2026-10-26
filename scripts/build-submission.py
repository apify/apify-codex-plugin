#!/usr/bin/env python3
"""Build and inspect the public MCP-only candidate using an explicit allowlist."""

import argparse
import hashlib
import json
import re
import stat
import struct
from pathlib import Path
from urllib.parse import urlencode, urlparse
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_FILES = ("plugin.json", "mcp.json", "assets/logo.png")
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
FORBIDDEN_SELECTORS = {"call-actor", "add-actor", "get-actor", "search-actors", "fetch-actor-details"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_source(root, relative):
    path = root / relative
    require(not any(p.is_symlink() for p in [path, *path.parents] if p != root.parent), f"Symlink source rejected: {relative}")
    require(path.is_file(), f"Missing regular source: {relative}")
    return path.read_bytes()


def https_url(value):
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password and not parsed.fragment


def validate_manifest(manifest, selectors):
    require(manifest.get("$schema") == PLUGIN_SCHEMA, "Portable plugin schema is required")
    require(manifest.get("name") == "apify", "Preserve the apify plugin identity")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest.get("version", "")), "Explicit semantic version is required")
    require(not {"skills", "hooks", "apps", "interface", "mcpServers"} & manifest.keys(), "Legacy or private components must not enter the portable manifest")
    extension = manifest["extensions"]["com.openai"]
    require(not {"apps", "hooks", "skills"} & extension.keys(), "Private bindings or execution components are prohibited")
    listing = extension["interface"]
    for field, maximum in [("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)]:
        require(isinstance(listing.get(field), str) and 0 < len(listing[field]) <= maximum, f"Invalid listing {field}")
    require(listing.get("category") == "Data & Analytics", "Preserve the selected listing category")
    for field in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
        require(isinstance(listing.get(field), str) and len(listing[field]) <= 1024 and https_url(listing[field]), f"Invalid listing {field}")
    prompts = listing["defaultPrompt"]
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "Supply one to three listing prompts")
    require(all(isinstance(p, str) and p.strip() and len(p) <= 128 and "\n" not in p for p in prompts), "Invalid listing prompt")
    require(len({" ".join(p.split()) for p in prompts}) == len(prompts), "Duplicate listing prompts")
    require(isinstance(listing.get("capabilities"), list) and all(isinstance(v, str) and v.strip() for v in listing["capabilities"]), "Invalid capabilities")
    for field in ["logo", "composerIcon"]:
        require(listing.get(field) == "./assets/logo.png", "Icon must use the allowlisted PNG")
    cases = extension["review"]["test_cases"]
    require(len(cases.get("positive", [])) >= 5 and len(cases.get("negative", [])) >= 3, "Need five positive and three negative cases")
    for group in ["positive", "negative"]:
        fields = ["description", "prompt"] + (["tools_triggered", "expected_behavior"] if group == "positive" else [])
        for case in cases[group]:
            require(all(isinstance(case.get(f), str) and case[f].strip() for f in fields), f"Incomplete {group} case")
            require(not {"status", "result", "passed"} & case.keys(), "Test results belong in evidence notes, not manifest cases")
            if group == "positive":
                require(any(name in case["tools_triggered"] for name in selectors), "Case names no contract tool")
    require(extension.get("publication", {}).get("release_notes"), "Release notes are required")


def create_payload(root):
    manifest_bytes = read_source(root, "submission/plugin.json")
    manifest = json.loads(manifest_bytes)
    contract = json.loads(read_source(root, "submission/tool-contract.json"))
    selectors = contract.get("selectors", [])
    require(len(selectors) == 29 and len(set(selectors)) == 29, "Expected exactly 29 unique tool selectors")
    require(all(re.fullmatch(r"[a-z][a-z0-9-]+", s) for s in selectors), "Selectors must be explicit tool names")
    require(not FORBIDDEN_SELECTORS.intersection(selectors), "Generic execution or discovery must not enter the contract")
    require(contract.get("baseUrl") == "https://mcp.apify.com/" and contract.get("client") == "openai", "Unexpected endpoint identity")
    validate_manifest(manifest, selectors)
    icon = read_source(root, "submission/assets/logo.png")
    require(icon[:8] == b"\x89PNG\r\n\x1a\n" and icon[12:16] == b"IHDR", "Submission icon must be PNG")
    width, height = struct.unpack(">II", icon[16:24])
    require(width == height and 256 <= width <= 4096 and len(icon) <= 5 * 1024 * 1024, "Invalid listing icon dimensions or size")
    server_url = contract["baseUrl"] + "?" + urlencode({"tools": ",".join(selectors), "client": contract["client"]})
    mcp = {
        "$schema": MCP_SCHEMA,
        "mcpServers": {
            "apify": {
                "type": "streamable-http",
                "url": server_url,
                "extensions": {"com.openai": {"auth": {"type": "oauth"}}},
            }
        },
    }
    payload = {"plugin.json": manifest_bytes, "mcp.json": (json.dumps(mcp, indent=2) + "\n").encode(), "assets/logo.png": icon}
    return payload, manifest, contract


def inspect_archive(path, expected):
    with ZipFile(path) as archive:
        expected_names = {f"apify/{name}" for name in ARCHIVE_FILES}
        require(set(archive.namelist()) == expected_names and len(archive.infolist()) == len(expected_names), "Archive inventory differs from explicit allowlist")
        require(archive.testzip() is None, "Archive CRC check failed")
        for entry in archive.infolist():
            require(not stat.S_ISLNK(entry.external_attr >> 16), "Archive contains a symlink")
            require(not entry.flag_bits & 1, "Archive must not be encrypted")
            require(archive.read(entry) == expected[entry.filename.removeprefix("apify/")], "Archived content differs from validated source")


def build(root=ROOT, destination=None):
    payload, manifest, contract = create_payload(root)
    destination = destination or root / "dist" / f"apify-chatgpt-plugin-{manifest['version']}-candidate.zip"
    require(not destination.resolve().is_relative_to((root / "submission").resolve()), "Archive must be outside submission source")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for name in ARCHIVE_FILES:
            info = ZipInfo(f"apify/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload[name])
    inspect_archive(destination, payload)
    readiness = json.loads(read_source(root, "submission/readiness.json"))
    report = {
        "archive": destination.name,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "files": [f"apify/{f}" for f in ARCHIVE_FILES],
        "toolCount": len(contract["selectors"]),
        "packageValidation": "passed-local-structural-checks",
        "submissionReady": False,
        "deploymentStatus": contract["deploymentStatus"],
        "reviewCases": readiness["reviewCases"],
        "gaps": readiness["gaps"],
    }
    destination.with_suffix(".readiness.json").write_text(json.dumps(report, indent=2) + "\n")
    return destination, report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    archive_path, result = build(destination=args.output)
    print(f"Created {archive_path}: {len(ARCHIVE_FILES)} allowlisted files, {result['toolCount']} selectors.")
    print("Local structure passed. INCOMPLETE CANDIDATE: live review cases, deployment, and submission requirements remain unverified.")
