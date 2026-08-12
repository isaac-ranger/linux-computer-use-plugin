#!/usr/bin/env python3
"""Perform a non-mutating MCP handshake and verify the advertised tool set."""

from __future__ import annotations

import json
import pathlib
import select
import subprocess
import sys
import time


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "linux-computer-use"
LAUNCHER = PLUGIN / "bin" / "launch-computer-use-linux.sh"
EXPECTED_TOOLS = {
    "activate_window",
    "click",
    "doctor",
    "drag",
    "focused_window",
    "get_app_state",
    "list_apps",
    "list_windows",
    "move_window",
    "perform_action",
    "press_key",
    "resize_window",
    "screenshot",
    "scroll",
    "set_value",
    "setup_accessibility",
    "setup_window_targeting",
    "type_text",
}


def send(process: subprocess.Popen[str], message: dict[str, object]) -> None:
    assert process.stdin is not None
    process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    process.stdin.flush()


def receive(process: subprocess.Popen[str], message_id: int, timeout: float = 8.0) -> dict[str, object]:
    assert process.stdout is not None
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        ready, _, _ = select.select([process.stdout], [], [], max(0.0, deadline - time.monotonic()))
        if not ready:
            break
        line = process.stdout.readline()
        if not line:
            break
        message = json.loads(line)
        if message.get("id") == message_id:
            return message
    raise TimeoutError(f"timed out waiting for MCP response id={message_id}")


def main() -> int:
    process = subprocess.Popen(
        [str(LAUNCHER), "mcp"],
        cwd=PLUGIN,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        send(
            process,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "plugin-check", "version": "1.0"},
                },
            },
        )
        initialized = receive(process, 1)
        if "error" in initialized:
            raise RuntimeError(initialized["error"])

        send(process, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        send(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        listed = receive(process, 2)
        tools = {
            tool["name"]
            for tool in listed.get("result", {}).get("tools", [])
            if isinstance(tool, dict) and isinstance(tool.get("name"), str)
        }
        missing = EXPECTED_TOOLS - tools
        if missing:
            raise RuntimeError(f"missing expected tools: {sorted(missing)}")
        print(f"MCP handshake passed: {len(tools)} tools advertised")
        return 0
    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"MCP handshake failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
