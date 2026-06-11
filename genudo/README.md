# Genudo AI — MCP Integration

This directory holds configuration and notes for connecting this repository to
the **Genudo AI** account (**"Food Good"**) over the Model Context Protocol (MCP).

## What's configured

The MCP server is registered in [`.mcp.json`](../.mcp.json) at the repo root:

```json
{
  "mcpServers": {
    "genudo": {
      "type": "http",
      "url": "https://fymcfqykdtxkhhwvszqg.supabase.co/functions/v1/genudo-mcp",
      "headers": {
        "Authorization": "Bearer ${GENUDO_API_KEY}"
      }
    }
  }
}
```

The bearer token is **not** hard-coded — it is read from the `GENUDO_API_KEY`
environment variable so the secret never gets committed to git.

## Setup — two things are required

### 1. Provide the API key as an environment variable

Set `GENUDO_API_KEY` to your Genudo key in the environment where Claude Code runs.

- **Local (shell):**
  ```bash
  export GENUDO_API_KEY="gnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ```
- **Claude Code on the web:** add `GENUDO_API_KEY` as an environment variable in
  the environment's configuration (Settings → Environment variables).

> Keep the key secret. Never paste it into a file that gets committed, into a
> PR description, or into a public channel. If it has been shared in plain text,
> rotate it in the Genudo dashboard.

### 2. Allow the Genudo host through the network policy

Claude Code's remote (web) execution environment enforces an outbound network
allowlist. The Genudo endpoint host must be allowed or the connection is blocked:

```
host: fymcfqykdtxkhhwvszqg.supabase.co
```

Add this host to the environment's network allowlist (or use a network policy
that permits it). See the docs:
https://code.claude.com/docs/en/claude-code-on-the-web

## Connecting / verifying

Once the key is set and the host is allowed, the `genudo` MCP server is picked up
automatically on the next Claude Code session start. Its tools appear as
`mcp__genudo__*`. You can then ask Claude to list the available Genudo tools and
operate on the **Food Good** account.
