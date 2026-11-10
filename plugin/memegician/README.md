# Memegician plugin for Claude

Make memes in Claude from 400+ classic templates. Claude finds the format that fits your situation,
writes captions in that format's traditional style and renders the finished image with a permanent
link you can share. Images are the stock templates with text drawn on them; no AI image generation.

## What's inside

- **Memegician MCP server** (`https://memegician.ai/mcp`): search templates, read a template's text
  slots, render memes, see trending formats, and (signed in) generate 6 ready-made memes at once.
- **make-memes skill**: how to pick a format, write captions that fit it and choose the right size
  for each platform.

## Use it

Ask things like:

- "Make a meme about Monday meetings using a trending template."
- "Drake meme: tabs vs spaces."
- "Give me 6 memes about my code working on the first try." (uses `generate_memes`, 1 credit)

The first four tools are free with no account (25 watermarked renders a day). `generate_memes` asks
you to sign in to Memegician the first time (Google or email code); new accounts get 15 credits and
paid plans are watermark-free. Disconnect any time under Profile → Connected apps on memegician.ai.

## Install

- **Claude Code:** `/plugin marketplace add Notysoty/memegician-mcp`, then `/plugin install memegician@memegician`
- **Claude (web/desktop):** zip this folder and upload it under Customize → Plugins, or add the
  connector `https://memegician.ai/mcp` under Settings → Connectors.

Docs: https://memegician.ai/mcp-server · Privacy: https://memegician.ai/privacy ·
Support: support@memegician.ai

## License

MIT
