# Apify for Codex

Official Apify plugin for Codex - adds the Apify MCP server and five bundled skills for the main Apify workflows: building and deploying Actors, actorizing existing projects, generating Actor output schemas, integrating Apify into existing applications, and running pre-built Apify Actors for data extraction.

> **Apify** is a platform of thousands of serverless cloud programs called **Actors** for web scraping, browser automation, and data extraction. Learn more at [apify.com](https://apify.com).

## What you get

| Component | Name | Purpose |
|---|---|---|
| Plugin manifest | `.codex-plugin/plugin.json` | Declares the Codex plugin package, metadata, bundled skills, and MCP configuration. |
| MCP server | `apify` (`https://mcp.apify.com/`) | Lets Codex search the Apify Store, fetch Actor details, run Actors, and read the Apify docs. |
| Skill | `apify-actor-development` | Create, debug, and deploy a brand new Apify Actor from scratch. |
| Skill | `apify-actorization` | Convert an existing JS/TS, Python, or CLI project into an Apify Actor. |
| Skill | `apify-generate-output-schema` | Generate `dataset_schema.json` / `output_schema.json` / `key_value_store_schema.json` for an existing Actor. |
| Skill | `apify-sdk-integration` | Add Apify Actor execution to an existing application using the `apify-client` package. |
| Skill | `apify-ultimate-scraper` | CLI-driven data extraction workflow for selecting, configuring, and running pre-built Actors across 15+ platforms. |

## Installation

Clone the plugin repo (or copy this folder as-is) and install it with the standard Codex plugin flow from the plugin root directory. Keep the package layout intact so Codex can resolve `.codex-plugin/plugin.json`, `.mcp.json`, `skills/`, and `assets/`.

```bash
git clone https://github.com/apify/codex-plugin /tmp/apify-codex-plugin
```

### Prerequisites

- **Codex** with plugin support enabled.
- Network access to `https://mcp.apify.com` for MCP-backed workflows.

## First-run setup

This plugin uses **three setup paths** depending on which bundled skill or MCP workflow Codex uses.

### Path 1 - Using existing Actors through MCP

Uses **OAuth**. The first time Codex calls a tool that needs auth (for example `run-actor` or `get-dataset-items`), it opens `console.apify.com` in your browser and asks you to sign in. Read-only tools such as `search-actors`, `fetch-actor-details`, `search-apify-docs`, and `fetch-apify-docs` work without auth.

### Path 2 - CLI workflows for Actor development, actorization, or scraper runs

These skills expect the local `apify` CLI to be available. Install it first:

```bash
npm install -g apify-cli
```

For interactive use, authenticate with:

```bash
apify login
```

In headless or CI environments, export an **`APIFY_TOKEN`** instead; the CLI can read it automatically:

```bash
export APIFY_TOKEN="apify_api_xxxxxxxxxxxx"
```

Generate a token at [console.apify.com/settings/integrations](https://console.apify.com/settings/integrations). Don't have an account? [Sign up free](https://console.apify.com/sign-up) - no credit card required.

### Path 3 - SDK integration into an existing application

Uses an **`APIFY_TOKEN`** environment variable with the `apify-client` package or the REST API:

```bash
export APIFY_TOKEN="apify_api_xxxxxxxxxxxx"
```

### Working in headless / SSH environments (no browser)

The MCP OAuth flow needs a browser. If you're running Codex in an environment without a browser, you have these options:

1. **Authenticate locally first.** Run a browser-capable Codex session once so the OAuth refresh token is stored, then reconnect remotely.
2. **Use the CLI-based skills.** `apify-actor-development`, `apify-actorization`, and `apify-ultimate-scraper` can work in headless environments when the `apify` CLI is installed and `APIFY_TOKEN` is exported.
3. **Use the SDK integration skill.** `apify-sdk-integration` uses `apify-client` and only needs `APIFY_TOKEN`.

## How to use it

Start a Codex session and describe what you need. This bundle does not include a dedicated routing agent, so it helps to be explicit about the workflow you want: use existing Actors, build an Actor, actorize a project, generate output schemas, or integrate Apify into an app.

```
find me 5 well-rated coffee shops in Seattle and export to CSV
build me an Actor that scrapes a sitemap and stores titles
add Apify to this Next.js app so I can run a scraper from /api/scrape
generate output schemas for the Actor in this folder
```

## Components reference

### MCP server

The `apify` MCP server is configured in `.mcp.json` and exposes:

- `search-actors` - search the Apify Store by keyword (no auth)
- `fetch-actor-details` - Actor specs, input schema, pricing (no auth)
- `run-actor` - execute an Actor and return results (OAuth)
- `get-dataset-items` - retrieve dataset rows from a previous run (OAuth)
- `search-apify-docs` / `fetch-apify-docs` - Apify documentation lookup

### Bundled scripts

This Codex plugin export does **not** include standalone helper scripts or a separate routing agent. Instead, the bundled skills ship with markdown references that Codex uses while working:

- `skills/apify-actor-development/references/` - Actor config, schemas, logging, standby mode, and README guidance
- `skills/apify-actorization/references/` - JS/TS, Python, and CLI actorization guides plus schema/output notes
- `skills/apify-ultimate-scraper/references/` - Actor index, gotchas, and workflow playbooks for common scraping use cases

The executable requirements come from the skills themselves: MCP-backed tasks use `.mcp.json`, CLI workflows rely on the local `apify` CLI, and `apify-sdk-integration` uses the `apify-client` SDK.

## Troubleshooting

**OAuth browser never opens / hangs.** See the "Working in headless / SSH environments" section above and switch to a CLI- or SDK-based path if needed.

**`apify` CLI not found.** Install it with `npm install -g apify-cli` before using `apify-actor-development`, `apify-actorization`, or `apify-ultimate-scraper`.

**`APIFY_TOKEN` not found.** Export `APIFY_TOKEN` in your shell before starting Codex when using headless CLI auth or the `apify-sdk-integration` skill.

**Codex keeps using the wrong skill.** This bundle exposes the skills directly rather than routing through a single `apify` agent, so describe the goal more explicitly: use existing Actors, build an Actor, actorize a project, generate output schemas, or integrate Apify into an app.

**`apify` vs `apify-client`** - these are two different npm packages. The `apify` package is the SDK for **building** Actors (used inside an Actor's code, on the Apify platform). The `apify-client` package is the API client for **calling** Actors from your own application. The bundled skills use the correct one for each workflow.

## Resources

- Apify Console - [console.apify.com](https://console.apify.com)
- Apify Store - [apify.com/store](https://apify.com/store)
- Docs (LLM-friendly) - [docs.apify.com/llms.txt](https://docs.apify.com/llms.txt)
- Docs (full) - [docs.apify.com/llms-full.txt](https://docs.apify.com/llms-full.txt)
- Source repo - [github.com/apify/codex-plugin](https://github.com/apify/codex-plugin)
- Issues / feedback - open an issue on the source repo, or email [support@apify.com](mailto:support@apify.com)

## License

Apache-2.0.
