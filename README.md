# Apify for Codex

The official [Apify plugin for Codex](https://github.com/apify/apify-codex-plugin) connects Codex to Apify's library of [Actors](https://apify.com/store). It bundles:

- The [Apify MCP server](https://docs.apify.com/platform/integrations/mcp) for searching the Store, running Actors, retrieving datasets, and reading Apify documentation.
- Five built-in skills for common Apify workflows.

> **Apify** is the largest marketplace of tools for AI: ready-made **Actors** you can run, or build your own. Find your Actor at [Apify Store](https://apify.com/store).

This guide covers installation in both the Codex app and Codex CLI.

## Prerequisites

- [An Apify account](https://console.apify.com/sign-up) - sign up for free if you don't have one.
- [Codex](https://developers.openai.com/codex/) - install the Codex app or Codex CLI with plugin support enabled.
- Network access to `https://mcp.apify.com` for MCP-backed workflows.

## Install the plugin

### Codex app

1. In Codex, open the left sidebar and select **Plugins**.
1. On the **Plugins** screen, select the dropdown next to **+** and choose **Add marketplace**.
1. In the **Add plugin marketplace** dialog, enter the Apify plugin repository in the **Source** field:

    ```text
    apify/apify-codex-plugin
    ```

1. Select **Add marketplace**.
1. On the **Plugins** screen, open the **Personal** tab. The **Apify** plugin appears under **Apify Plugin**.
1. Select **Add** next to **Apify**.
1. In the dialog, select **Add to Codex**.
1. Select **Install Apify** to start the Apify MCP server setup.

### Codex CLI

1. In the Codex CLI, run the `/plugins` command.
1. Use the arrow keys to move right to the **Add Marketplace** tab, then press Enter.
1. Type the Apify plugin repository and press Enter:

    ```text
    apify/apify-codex-plugin
    ```

1. Open the **Apify Plugin** tab, select **Apify**, and press Enter to view the plugin details.
1. Select **Install plugin** and press Enter.

## Authenticate to Apify

The plugin bundles the Apify MCP server. Read-only tools such as searching the Store and fetching Actor details work without signing in. Authentication is required to run Actors and access your account data.

### Codex app

1. After you select **Install Apify**, Codex starts the Apify MCP server setup and opens a browser tab for the Apify OAuth flow.
1. Review the permissions and select **Allow access**.
1. Return to Codex. The `apify` MCP server is connected and ready to use.

### Codex CLI

1. The first time Codex calls a tool that requires authentication, such as running an Actor, it opens a browser tab for the Apify OAuth flow.
1. Review the permissions and select **Allow access**.
1. Return to the terminal. The `apify` MCP server is connected and ready to use in any new chat.

The connection stays authenticated for future sessions. You can revoke access at any time in [Apify Console > Settings > Integrations](https://console.apify.com/settings/integrations).

### CLI-based skills and SDK integration

The `apify-actor-development`, `apify-actorization`, and `apify-ultimate-scraper` skills use the local Apify CLI. Install and authenticate it before using these workflows:

```bash
npm install -g apify-cli
apify login
```

The `apify-sdk-integration` skill and headless CLI workflows use an `APIFY_TOKEN`. Generate one in [Apify Console](https://console.apify.com/settings/integrations), then export it before starting Codex:

```bash
export APIFY_TOKEN="apify_api_xxxxxxxxxxxx"
```

## Run your first prompt

In a Codex app or Codex CLI chat, describe what you want in natural language. Because the plugin exposes its MCP tools and skills directly, be explicit about the workflow:

> Use Apify to find a good Actor for scraping Google Maps places. Show me the best option, its input requirements, pricing model, and what kind of dataset output it returns. Do not run the Actor yet.

Codex searches Apify Store, fetches the top Actor's details through the `apify` MCP server, and summarizes its inputs, pricing, and output without running the Actor.

## Bundled skills

| Skill | Description |
| --- | --- |
| `apify-ultimate-scraper` | CLI-driven extraction using existing Actors for multi-step scraping and lead-generation workflows. |
| `apify-actor-development` | Full Actor lifecycle - template selection, development, local testing, and deployment with `apify push`. |
| `apify-actorization` | Converts existing JavaScript, TypeScript, Python, or CLI projects into Apify Actors. |
| `apify-generate-output-schema` | Generates dataset and key-value store schemas for existing Actors. |
| `apify-sdk-integration` | Integrates Actor execution into applications using the `apify-client` package. |

Example prompts that route to specific skills:

_Ultimate scraper:_

> Find 10 highly rated coffee shops in Seattle with name, address, rating, phone, and website.

_Actor development:_

> Create an Apify Actor that accepts a `startUrl` and `maxPages` input, crawls the site, and stores each page title and URL.

_SDK integration:_

> Add Apify to this project. The Node.js API route should run an Actor and return dataset items as JSON.

## Troubleshooting

### The Plugins screen or `/plugins` command does not appear

Plugins require a local Codex installation with plugin support enabled. Install or update Codex, then reopen the **Plugins** screen or run `/plugins` again.

### The Apify plugin does not appear

Confirm that the Apify marketplace was added. In the Codex app, check the **Personal** tab. In the Codex CLI, check the **Apify Plugin** tab. If the plugin still does not appear, re-add the marketplace using `apify/apify-codex-plugin`.

### The browser does not open, or OAuth fails

Copy the OAuth URL shown by Codex and open it manually. In a headless environment such as SSH or a remote container, copy your token from [Apify Console](https://console.apify.com/settings/integrations) and set it before starting Codex:

```bash
export APIFY_TOKEN=<YOUR_API_TOKEN>
```

### The `apify` CLI is not found

Install it with `npm install -g apify-cli` before using `apify-actor-development`, `apify-actorization`, or `apify-ultimate-scraper`.

### Codex uses the wrong skill

Describe the workflow more explicitly: use an existing Actor, build an Actor, actorize a project, generate output schemas, or integrate Apify into an application.

## Limitations

- Long-running Actors may exceed the time a single tool call waits for completion. Reduce the scope or split the work across multiple prompts.
- Each Actor run consumes Apify platform usage from your plan in addition to any Codex usage.
- Skills that edit project files make local changes. Review them before deploying or committing.

## Resources

- [Apify plugin for Codex](https://github.com/apify/apify-codex-plugin)
- [Codex documentation](https://developers.openai.com/codex/)
- [Apify Store](https://apify.com/store)
- [Apify Console](https://console.apify.com)
- [Apify documentation for LLMs](https://docs.apify.com/llms.txt)

## License

Apache-2.0.
