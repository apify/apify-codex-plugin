# Public submission candidate

This directory owns the portable, MCP-only Apify public upload. The existing
Codex marketplace distribution remains in `apify/` and retains its skills.

The candidate is **incomplete and not ready to submit**. The selected endpoint
uses 29 explicit tool selectors on `https://mcp.apify.com/`; the new selectors
are not deployed. Curated execution also needs approved builds before it can
run. See `readiness.json` for the remaining review work.

## Build and inspect

Run these commands in an isolated Python 3.13 environment from the repository
root. They use only Python's standard library and make no network requests:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/build-submission.py
```

The builder writes `dist/apify-chatgpt-plugin-1.2.0-candidate.zip` and an adjacent
readiness report. It reads the tool list from `tool-contract.json`, generates
portable `mcp.json`, and includes exactly:

```text
apify/plugin.json
apify/mcp.json
apify/assets/logo.png
```

The archive inventory is an explicit allowlist. Skills, hooks, compatibility
manifests, marketplace files, private app bindings, source code, and review
notes cannot enter the archive through directory recursion. The builder checks
the final ZIP bytes as well as its source files. Local checks verify structure;
they do not establish portal acceptance or live behavior.

`assets/logo.png` is a 408-by-408 rasterization of the supplied
`apify/assets/logo.svg`, with the artwork unchanged.

## Review evidence and next steps

The five positive and three negative cases are stored in the manifest at
`extensions.com.openai.review.test_cases`. **All eight cases are Not run.**
Use a dedicated test account and agree a budget before running billable tests.
Record tool arguments, returned results, and pass/fail evidence outside the ZIP.
The supplemental [review matrix](./review-matrix.md) covers the 13 curated tools,
private source edits, revision conflicts, ownership checks, and build selection.

The initial recording should show the exact candidate version in ChatGPT,
OAuth sign-in with credentials hidden, sitemap extraction, one public listing
query, the private greeting Actor's build and test, and a rejected publishing
request. Rehearse after the server deployment, record real results, then inspect
playback and reviewer access before adding `review.demo_recording_url`.

The four listing URLs identify Apify and its existing support and policies.
The authorized owner still needs to verify coverage of the submitted data
flows. Commerce declarations, the demo URL, and legal attestations remain
unresolved. Reviewer credentials belong only in secure portal fields. The
publisher explicitly selected all portal-supported countries: the portable
manifest records `publication.countries: []` to remove country restrictions.
Verify that choice in the saved portal draft before submission.

## Repository rename

Rename the existing GitHub repository to `apify-chatgpt-plugin`; preserve its
repository ID `1237525987`, history, releases, and installed marketplace identity.
The local work so far has not performed the remote rename.

1. Merge the upstream sync resolution guard in `apify-plugins-internal` first.
   It accepts the old and new names only for the verified repository ID and
   keeps generated skills under `apify/`.
2. Have an administrator rename the existing repository. Do not create a
   replacement repository with a different identity.
3. Verify the canonical GitHub name and service-account access. Update the
   `repository` URL in `submission/plugin.json`, the existing compatibility
   manifest, and README installation links to the verified new URL.
4. Run upstream sync in dry-run mode and inspect that it still targets `apify/`.
   Rebuild this archive and retest marketplace installation after the rename.

The current metadata uses the verified old repository URL until step three.
The public display name stays **Apify**, and the package name stays `apify`.
The existing developer release workflow accepts either name only for the same
immutable repository ID, so renaming does not disable its manual release path.
Public submission versions and uploads remain separate from that workflow.
