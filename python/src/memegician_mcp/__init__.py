"""memegician-mcp: a stdio bridge to the hosted Memegician MCP server.

MCP clients that only launch local commands run this; it forwards each JSON-RPC message
to https://memegician.ai/mcp (Streamable HTTP, stateless) and writes the responses back
to stdout. Standard library only, Python 3.8+.

Env: MEMEGICIAN_API_KEY  optional: watermark-free renders, and generate_memes without signing in
                         (Startup/Enterprise key from https://memegician.ai/api-access)
     MEMEGICIAN_MCP_URL  optional, defaults to https://memegician.ai/mcp
"""
import json
import os
import platform
import sys
import urllib.error
import urllib.request

__version__ = "1.1.0"
SIGN_IN_HELP = (
    "This tool needs a Memegician account. Local (stdio) setups can't sign in, so either "
    "connect https://memegician.ai/mcp as a remote connector (your app will ask you to sign in; new accounts get 15 free credits) "
    "or set MEMEGICIAN_API_KEY to a Startup/Enterprise API key from https://memegician.ai/api-access. "
    "The free tools (search_meme_templates, get_meme_template, render_meme, get_trending_meme_templates) work without either."
)
ENDPOINT = os.environ.get("MEMEGICIAN_MCP_URL", "https://memegician.ai/mcp")
API_KEY = os.environ.get("MEMEGICIAN_API_KEY", "")


def _write(message):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def _calls(request):
    messages = request if isinstance(request, list) else [request]
    return [m for m in messages if isinstance(m, dict) and m.get("id") is not None]


def forward(line, state):
    try:
        request = json.loads(line)
    except ValueError:
        return
    calls = _calls(request)
    ids = [m["id"] for m in calls]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "memegician-mcp/%s (stdio bridge; python %s)" % (__version__, platform.python_version()),
    }
    if API_KEY:
        headers["Authorization"] = "Bearer " + API_KEY
    if state.get("protocol"):
        headers["MCP-Protocol-Version"] = state["protocol"]
    req = urllib.request.Request(ENDPOINT, data=line.encode("utf-8"), headers=headers, method="POST")
    try:
        try:
            res = urllib.request.urlopen(req, timeout=120)
            status, body, ctype = res.status, res.read().decode("utf-8"), res.headers.get("Content-Type", "")
        except urllib.error.HTTPError as err:  # 4xx/5xx still carry a JSON-RPC error body
            status, body, ctype = err.code, err.read().decode("utf-8"), err.headers.get("Content-Type", "")
        if status in (202, 204) or not body.strip():
            return
        # A sign-in challenge (OAuth 401) isn't a JSON-RPC message: answer each request with help instead
        if status == 401 and '"jsonrpc"' not in body:
            for m in calls:
                if m.get("method") == "tools/call":
                    _write({"jsonrpc": "2.0", "id": m["id"], "result": {"isError": True, "content": [{"type": "text", "text": SIGN_IN_HELP}]}})
                else:
                    _write({"jsonrpc": "2.0", "id": m["id"], "error": {"code": -32001, "message": SIGN_IN_HELP}})
            return
        if "text/event-stream" in ctype:
            payloads = [l[5:].strip() for l in body.splitlines() if l.startswith("data:")]
        else:
            payloads = [body]
        for payload in payloads:
            if not payload:
                continue
            message = json.loads(payload)
            for m in message if isinstance(message, list) else [message]:
                if isinstance(m, dict):
                    proto = (m.get("result") or {}).get("protocolVersion") if isinstance(m.get("result"), dict) else None
                    if proto:
                        state["protocol"] = proto
                    if m.get("error") and m.get("id") is None and len(ids) == 1:
                        m["id"] = ids[0]
            _write(message)
    except Exception as err:  # network errors: answer each request so the client doesn't hang
        for i in ids:
            _write({"jsonrpc": "2.0", "id": i, "error": {"code": -32603, "message": "Memegician MCP server unreachable: %s" % err}})


def main():
    state = {}
    for line in sys.stdin:
        if line.strip():
            forward(line.strip(), state)


if __name__ == "__main__":
    main()
