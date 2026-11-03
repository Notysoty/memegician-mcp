#!/usr/bin/env bash
# Copy the shared README and LICENSE into both packages before publishing.
# (The README carries "mcp-name: ai.memegician/memegician", which PyPI/npm listings in the
# official MCP Registry are verified against.)
set -euo pipefail
cd "$(dirname "$0")"
for d in npm python; do cp README.md LICENSE "$d/"; done
echo "README.md and LICENSE copied into npm/ and python/"
