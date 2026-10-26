import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

SPEC = importlib.util.spec_from_file_location("package_builder", Path(__file__).with_name("build-submission.py"))
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class SubmissionArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(BUILDER.ROOT / "submission", self.root / "submission")

    def tearDown(self):
        self.temp.cleanup()

    def alter(self, name, change):
        path = self.root / "submission" / name
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_archive_excludes_skills_hooks_private_bindings_and_unrelated_files(self):
        for relative in ["submission/skills/hidden/SKILL.md", "submission/hooks/hooks.json", "submission/.app.json", "submission/.codex-plugin/plugin.json", "apify/skills/existing/SKILL.md"]:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Must not enter the public archive")
        archive, report = BUILDER.build(self.root)
        with ZipFile(archive) as zipped:
            self.assertEqual(set(zipped.namelist()), {"apify/plugin.json", "apify/mcp.json", "apify/assets/logo.png"})
            manifest = json.loads(zipped.read("apify/plugin.json"))
            self.assertEqual(manifest["extensions"]["com.openai"]["publication"]["countries"], [])
            mcp = json.loads(zipped.read("apify/mcp.json"))
            self.assertIn("client=openai", mcp["mcpServers"]["apify"]["url"])
            self.assertEqual(mcp["mcpServers"]["apify"]["extensions"]["com.openai"]["auth"]["type"], "oauth")
        self.assertFalse(report["submissionReady"])
        self.assertEqual(report["reviewCases"], "Not run")

    def test_rebuild_is_deterministic(self):
        first, _ = BUILDER.build(self.root, self.root / "first.zip")
        second, _ = BUILDER.build(self.root, self.root / "second.zip")
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_rejects_legacy_and_private_manifest_components(self):
        self.alter("plugin.json", lambda manifest: manifest.update({"skills": "./skills"}))
        with self.assertRaisesRegex(ValueError, "Legacy or private"):
            BUILDER.build(self.root)

    def test_rejects_nested_app_bindings(self):
        self.alter("plugin.json", lambda manifest: manifest["extensions"]["com.openai"].update({"apps": "./.app.json"}))
        with self.assertRaisesRegex(ValueError, "Private bindings"):
            BUILDER.build(self.root)

    def test_rejects_generic_executor_or_duplicate_selectors(self):
        self.alter("tool-contract.json", lambda contract: contract["selectors"].__setitem__(0, "call-actor"))
        with self.assertRaisesRegex(ValueError, "Generic execution"):
            BUILDER.build(self.root)
        self.alter("tool-contract.json", lambda contract: contract["selectors"].__setitem__(0, contract["selectors"][1]))
        with self.assertRaisesRegex(ValueError, "29 unique"):
            BUILDER.build(self.root)

    def test_rejects_allowlisted_symlink(self):
        icon = self.root / "submission/assets/logo.png"
        content = icon.read_bytes()
        icon.unlink()
        outside = self.root / "outside.png"
        outside.write_bytes(content)
        icon.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            BUILDER.build(self.root)

    def test_rejects_tampered_archive(self):
        archive, _ = BUILDER.build(self.root)
        payload, _, _ = BUILDER.create_payload(self.root)
        with ZipFile(archive, "a") as zipped:
            zipped.writestr("apify/skills/bypass/SKILL.md", "unexpected")
        with self.assertRaisesRegex(ValueError, "inventory"):
            BUILDER.inspect_archive(archive, payload)

    def test_rejects_incomplete_cases(self):
        self.alter("plugin.json", lambda manifest: manifest["extensions"]["com.openai"]["review"]["test_cases"]["negative"].pop())
        with self.assertRaisesRegex(ValueError, "five positive"):
            BUILDER.build(self.root)

    def test_rejects_overlong_listing_subtitle(self):
        self.alter("plugin.json", lambda manifest: manifest["extensions"]["com.openai"]["interface"].update({"shortDescription": "x" * 31}))
        with self.assertRaisesRegex(ValueError, "shortDescription"):
            BUILDER.build(self.root)


if __name__ == "__main__":
    unittest.main()
