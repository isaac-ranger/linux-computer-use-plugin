# Linux Computer Use plugin

An unofficial Codex plugin and Git-backed marketplace for controlling a local
Linux desktop through the
[`computer-use-linux`](https://github.com/agent-sh/computer-use-linux) MCP
server.

The plugin can inspect accessibility trees and windows, capture screenshots,
focus and move windows, and send pointer or keyboard input. It supports GNOME,
KDE/KWin, Hyprland, i3, COSMIC, and best-effort generic X11 environments.

This project is not made, supported, or endorsed by OpenAI. It does not patch
ChatGPT or Codex, alter product entitlements, or bypass feature gates. It uses
Codex's documented plugin and bundled-MCP mechanisms.

## Security warning

Installing this plugin gives the active Codex host tools that can observe and
control your desktop. Screenshots and accessibility trees may contain private
information. Clicks and keystrokes can submit forms, send messages, delete
data, or make purchases in whatever application is targeted.

The MCP server advertises mutating and destructive tool annotations. The
bundled skill additionally requires explicit confirmation before actions that
send, submit, purchase, delete, overwrite, publish, or otherwise create a
difficult-to-reverse result. Those controls reduce risk; they are not a
security boundary. Only install this plugin on a machine and account you trust.

## Install

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add isaac-ranger/linux-computer-use-plugin
codex plugin add linux-computer-use@linux-computer-use
```

Restart the ChatGPT desktop app or start a new Codex session after installing.
Then ask:

```text
@linux-computer-use Check whether Linux Computer Use is ready.
```

The plugin bundles verified upstream binaries for Linux x86_64 and aarch64.
It does not download or compile code during installation or launch.

## Desktop prerequisites

Run the read-only readiness check first:

```text
@linux-computer-use Run the Computer Use doctor and explain any blockers.
```

Typical requirements are:

- AT-SPI accessibility services for semantic application trees.
- A supported desktop portal or screenshot backend.
- `/dev/uinput`, a RemoteDesktop portal, `xdotool`, or `ydotool` for input.
- The optional upstream GNOME Shell extension for exact window targeting on
  GNOME sessions where Shell Introspect is restricted.

Setup tools change user-session configuration. Review their proposed changes
before approving them.

## Provenance

The packaged MCP binaries are the unmodified release artifacts from:

- Upstream: <https://github.com/agent-sh/computer-use-linux>
- Release: [`v0.4.9`](https://github.com/agent-sh/computer-use-linux/releases/tag/v0.4.9)
- Source commit: `c60d5ae7d8d94b1712c25c776b2025024377c60b`
- License: MIT, copyright Avi Fenesh

Checksums are recorded in
[`plugins/linux-computer-use/bin/checksums.sha256`](plugins/linux-computer-use/bin/checksums.sha256).
The upstream license and attribution are included with the plugin.

## Validate locally

```bash
(cd plugins/linux-computer-use/bin && sha256sum -c checksums.sha256)
python3 -m json.tool plugins/linux-computer-use/.codex-plugin/plugin.json >/dev/null
sh -n plugins/linux-computer-use/bin/launch-computer-use-linux.sh
python3 scripts/check_mcp.py
```

During development, also run Codex's `plugin-creator` validator when it is
available. The commands above work in CI without Codex development files.

## Updating the backend

Backend updates should be deliberate and reviewable:

1. Pin a tagged `agent-sh/computer-use-linux` release and source commit.
2. Download both architecture variants and their COSMIC helpers.
3. Verify the upstream checksum files before replacing bundled assets.
4. Update `checksums.sha256`, `UPSTREAM.md`, and the plugin version.
5. Run the manifest, checksum, and MCP handshake checks.

## License

The marketplace wrapper and safety skill are MIT licensed. The bundled
`computer-use-linux` artifacts remain under their upstream MIT license; see
[`THIRD_PARTY_LICENSES/agent-sh-computer-use-linux-MIT.txt`](plugins/linux-computer-use/THIRD_PARTY_LICENSES/agent-sh-computer-use-linux-MIT.txt).
