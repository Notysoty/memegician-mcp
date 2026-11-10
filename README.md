# Memegician MCP server

Make memes inside **Claude, ChatGPT, Cursor, VS Code, Windsurf** and any MCP client. Your assistant writes the captions; Memegician finds the right template among 400+ classics and renders the image.

<!-- mcp-name: ai.memegician/memegician -->

- **Hosted server:** `https://memegician.ai/mcp` (Streamable HTTP, nothing to install)
- **Free tier (no key):** 500 template searches and 25 rendered memes a day (with a small `memegician.ai` watermark), plus trending templates
- **Sign in with Memegician** (optional): unlocks `generate_memes`, which writes 6 finished memes per call from your account credits (new accounts get 15 free). Your AI app shows a sign-in button the first time you use it.
- **With an API key** ([get one](https://memegician.ai/api-access), Startup or Enterprise plan): watermark-free renders; each render uses one API request
- **Docs:** https://memegician.ai/mcp-server · Official MCP Registry: `ai.memegician/memegician`

## Tools

| Tool | Input | Output |
|---|---|---|
| `search_meme_templates` | `query` (emotion, situation or name), `limit?` (1-25) | Template ids, names, slot counts, blank image URLs |
| `get_meme_template` | `template_id` | Text slots (what each caption is for, in order), description, when to use, example captions |
| `render_meme` | `template_id`, `captions[]`, `aspect_ratio?` (`1:1`, `3:4`, `4:3`, `9:16`, `16:9`) | The meme image plus a permanent PNG URL |
| `get_trending_meme_templates` | `limit?` | Most-searched templates in the latest month of US Google search data (the result names the month) and biggest risers |
| `generate_memes` (sign-in, 1 credit) | `situation` | 6 finished memes: AI picks the templates and writes the captions. Also saved to My Memes on memegician.ai |

Prompt: `make_meme` (`topic`, `tone?`).

The first four tools are free and need no account. Try: *"Make a meme about Monday meetings using a trending template."* Signed in: *"Generate memes about my code working on the first try."*

## Sign in (for `generate_memes`)

Memegician is a standard OAuth 2.1 authorization server for MCP (PKCE, Client ID Metadata Documents, dynamic client registration, resource-bound tokens). Remote connectors (Claude, ChatGPT, Claude Code, Cursor, VS Code) handle it for you:

1. Ask for something that uses `generate_memes`.
2. Your app shows **Connect** / **Sign in**. Log in to memegician.ai (Google or email code) and click **Allow**.
3. Ask again. Each call uses 1 credit; paid plans get watermark-free memes.

Manage or disconnect apps any time under **Profile → Connected apps** on memegician.ai. Local (stdio) setups can't sign in; use a Startup/Enterprise API key there.

## Connect (remote, recommended)

**Claude** (claude.ai / desktop): Settings → Connectors → Add custom connector → `https://memegician.ai/mcp`

**Claude Code:**
```bash
claude mcp add --transport http memegician https://memegician.ai/mcp
```

**Cursor** (`.cursor/mcp.json`) · **Windsurf** uses `serverUrl` instead of `url`:
```json
{ "mcpServers": { "memegician": { "url": "https://memegician.ai/mcp" } } }
```

**VS Code** (`.vscode/mcp.json`):
```json
{ "servers": { "memegician": { "type": "http", "url": "https://memegician.ai/mcp" } } }
```

Optional: add `"headers": { "Authorization": "Bearer YOUR_API_KEY" }` for watermark-free renders, or to use `generate_memes` without signing in (Startup/Enterprise key).

## Connect (local command)

For clients that only run local commands, use the stdio bridge. It forwards to the hosted server and has no dependencies.

**npm** (Node 18+):
```json
{ "mcpServers": { "memegician": { "command": "npx", "args": ["-y", "memegician-mcp"], "env": { "MEMEGICIAN_API_KEY": "optional" } } } }
```

**PyPI** (Python 3.8+):
```json
{ "mcpServers": { "memegician": { "command": "uvx", "args": ["memegician-mcp"], "env": { "MEMEGICIAN_API_KEY": "optional" } } } }
```

Leave `MEMEGICIAN_API_KEY` out to use the free tier. In local setups `generate_memes` needs the key (or connect the remote URL above and sign in).

## Privacy

Rendered memes get a permanent public URL so they can be shared. Signing in gives the AI app a token tied to your account and this server only; access tokens last 1 hour and you can revoke the app from Connected apps. Full policy: https://memegician.ai/privacy Don't put private information in captions. Free-tier captions pass an automated safety check.

## This repository

- `npm/`: the `memegician-mcp` npm package (stdio bridge)
- `python/`: the `memegician-mcp` PyPI package (stdio bridge)
- `server.json`: the entry in the [official MCP Registry](https://registry.modelcontextprotocol.io)
- `examples/`: client configs and a JSON-RPC smoke test (`node npm/bin/memegician-mcp.js < examples/test-messages.jsonl`)

The server itself is hosted by [Memegician](https://memegician.ai). Issues and feature requests are welcome.

## License

MIT
