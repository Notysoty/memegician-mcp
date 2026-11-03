# Memegician MCP server

Make memes inside **Claude, ChatGPT, Cursor, VS Code, Windsurf** and any MCP client. Your assistant writes the captions; Memegician finds the right template among 400+ classics and renders the image.

<!-- mcp-name: ai.memegician/memegician -->

- **Hosted server:** `https://memegician.ai/mcp` (Streamable HTTP, nothing to install)
- **Free tier (no key):** 500 template searches and 25 rendered memes a day (with a small `memegician.ai` watermark), plus trending templates
- **With an API key** ([get one](https://memegician.ai/api-access), Startup or Enterprise plan): watermark-free renders; each render uses one API request
- **Docs:** https://memegician.ai/mcp-server · Official MCP Registry: `ai.memegician/memegician`

## Tools

| Tool | Input | Output |
|---|---|---|
| `search_meme_templates` | `query` (emotion, situation or name), `limit?` (1-25) | Template ids, names, slot counts, blank image URLs |
| `get_meme_template` | `template_id` | Text slots (what each caption is for, in order), description, when to use, example captions |
| `render_meme` | `template_id`, `captions[]`, `aspect_ratio?` (`1:1`, `3:4`, `4:3`, `9:16`, `16:9`) | The meme image plus a permanent PNG URL |
| `get_trending_meme_templates` | `limit?` | This month's most-searched templates (US Google search volume) and biggest risers |

Prompt: `make_meme` (`topic`, `tone?`).

Try: *"Make a meme about Monday meetings using a trending template."*

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

Add `"headers": { "Authorization": "Bearer YOUR_API_KEY" }` for watermark-free renders.

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

Leave `MEMEGICIAN_API_KEY` out to use the free tier.

## Privacy

Rendered memes get a permanent public URL so they can be shared. Don't put private information in captions. Free-tier captions pass an automated safety check.

## This repository

- `npm/`: the `memegician-mcp` npm package (stdio bridge)
- `python/`: the `memegician-mcp` PyPI package (stdio bridge)
- `server.json`: the entry in the [official MCP Registry](https://registry.modelcontextprotocol.io)
- `examples/`: client configs and a JSON-RPC smoke test (`node npm/bin/memegician-mcp.js < examples/test-messages.jsonl`)

The server itself is hosted by [Memegician](https://memegician.ai). Issues and feature requests are welcome.

## License

MIT
