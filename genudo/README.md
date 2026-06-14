# Genudo

This directory holds Genudo AI integration assets for this repo.

## Genudo MCP server

The Genudo MCP server is configured in [`../.mcp.json`](../.mcp.json) at the repo
root so that Claude Code picks it up automatically when a session loads in this
repository.

```json
{
  "mcpServers": {
    "genudo": {
      "type": "http",
      "url": "https://fymcfqykdtxkhhwvszqg.supabase.co/functions/v1/genudo-mcp",
      "headers": {
        "Authorization": "Bearer ${GENUDO_TOKEN}"
      }
    }
  }
}
```

### Authentication

The `Authorization` header references the `GENUDO_TOKEN` environment variable
instead of hardcoding the key, so the credential is **never committed to git**.

Set the token in your environment before starting a session:

```bash
export GENUDO_TOKEN="gnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

For Claude Code on the web, add `GENUDO_TOKEN` as an environment secret in your
environment configuration rather than exporting it locally.

> **Note:** The MCP server is loaded when a Claude Code session starts. After
> the `GENUDO_TOKEN` is set and this config is in place, reload / start a new
> session for the `genudo` tools (e.g. the Fluent / account workspaces) to
> become available.
