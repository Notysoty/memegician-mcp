#!/usr/bin/env node
/**
 * memegician-mcp: a stdio bridge to the hosted Memegician MCP server.
 *
 * MCP clients that only launch local commands (e.g. Claude Desktop config files) run this;
 * it forwards each JSON-RPC message to https://memegician.ai/mcp (Streamable HTTP,
 * stateless) and writes the responses back to stdout. No dependencies, Node 18+.
 *
 * Env: MEMEGICIAN_API_KEY  optional, watermark-free renders (https://memegician.ai/api-access)
 *      MEMEGICIAN_MCP_URL  optional, defaults to https://memegician.ai/mcp
 */
"use strict";
const readline = require("node:readline");

const VERSION = "1.0.0";
const ENDPOINT = process.env.MEMEGICIAN_MCP_URL || "https://memegician.ai/mcp";
const API_KEY = process.env.MEMEGICIAN_API_KEY || "";
let protocolVersion = "";

function write(message) {
  process.stdout.write(JSON.stringify(message) + "\n");
}

async function forward(line) {
  let request;
  try { request = JSON.parse(line); } catch { return; }
  const ids = (Array.isArray(request) ? request : [request]).map((m) => m && m.id).filter((id) => id !== undefined && id !== null);
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json, text/event-stream",
    "User-Agent": `memegician-mcp/${VERSION} (stdio bridge; node ${process.version})`,
  };
  if (API_KEY) headers.Authorization = `Bearer ${API_KEY}`;
  if (protocolVersion) headers["MCP-Protocol-Version"] = protocolVersion;
  try {
    const res = await fetch(ENDPOINT, { method: "POST", headers, body: line });
    if (res.status === 202 || res.status === 204) return; // notification accepted
    const text = await res.text();
    const payloads = (res.headers.get("content-type") || "").includes("text/event-stream")
      ? text.split(/\r?\n/).filter((l) => l.startsWith("data:")).map((l) => l.slice(5).trim())
      : [text];
    for (const payload of payloads) {
      if (!payload) continue;
      const message = JSON.parse(payload);
      for (const m of Array.isArray(message) ? message : [message]) {
        if (m && m.result && m.result.protocolVersion) protocolVersion = m.result.protocolVersion;
        // HTTP-level errors come back with id null; give them the request's id
        if (m && m.error && (m.id === null || m.id === undefined) && ids.length === 1) m.id = ids[0];
      }
      write(message);
    }
  } catch (err) {
    for (const id of ids) write({ jsonrpc: "2.0", id, error: { code: -32603, message: `Memegician MCP server unreachable: ${err.message}` } });
  }
}

let queue = Promise.resolve();
const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.on("line", (line) => { if (line.trim()) queue = queue.then(() => forward(line)); });
// Let Node exit on its own once pending requests finish (process.exit can crash on Windows mid-close)
rl.on("close", () => { queue.then(() => { process.exitCode = 0; }); });
