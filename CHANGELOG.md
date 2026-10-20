# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0]

### Changed
- `.mcp.json` now uses the `mcpServers` wrapper required by the OpenAI plugin validator (Codex accepts both shapes).
- Shortened `interface.shortDescription` to fit the 30-character directory limit.
- Bumped manifest `version` to match this changelog.
- README: the hosted MCP server requires authentication for all tools in the plugin's default tool set; removed the claim that read-only tools work without signing in.

### Added
- `interface.defaultPrompt` with three starter prompts (required by the plugin validator and the submission portal).

## [1.0.1]

### Changed
- Updated Apify MCP server URL in `.mcp.json` to include `?client=codex+plugin` for client identification.

## [1.0.0] - Initial Codex release

### Added
- `.codex-plugin/plugin.json` manifest with Codex plugin metadata.
- `apify` MCP server entry in `.mcp.json` pointing to `https://mcp.apify.com/`.
- Apache-2.0 license.
