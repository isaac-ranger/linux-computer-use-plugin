# Security policy

## Reporting vulnerabilities

Please report wrapper, packaging, or marketplace vulnerabilities through a
private GitHub security advisory for this repository.

Report vulnerabilities in the MCP backend itself to the upstream
[`agent-sh/computer-use-linux` security process](https://github.com/agent-sh/computer-use-linux/security/policy).

Do not include screenshots, accessibility trees, credentials, tokens, or other
private desktop contents in a public issue.

## Trust model

This plugin runs a native MCP server as the current desktop user. Its tools can
observe the desktop and generate real keyboard and pointer input. Codex
sandboxing does not turn the desktop into a disposable environment.

The package contains pinned, checksum-verified upstream release binaries. It
does not self-update, download code at launch, install a persistent service, or
request root privileges. Desktop setup tools can still change user-session
configuration when the user approves them.
