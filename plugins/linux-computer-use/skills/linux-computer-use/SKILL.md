---
name: linux-computer-use
description: Inspect or control authorized local Linux desktop applications using the Linux Computer Use MCP tools.
---

# Linux Computer Use

Use these tools only for the local Linux desktop and applications the user is
authorized to access.

1. Begin every desktop-control turn with `get_app_state`. Use `doctor` first
   when readiness is unknown or `get_app_state` reports a blocker.
2. Prefer accessibility elements and semantic actions over pixel coordinates.
   Refresh application state before reusing an element index.
3. Before targeted keyboard input, identify and focus the intended window.
   Treat a focus-verification warning as failed input.
4. Read-only inspection may expose private screen or accessibility content.
   Return only what is necessary for the request and do not persist captured
   content unless the user explicitly asks.
5. Ask for explicit confirmation immediately before any action that could
   send, submit, purchase, delete, overwrite, publish, change permissions, or
   create another difficult-to-reverse effect. State the target and expected
   result in the confirmation request.
6. Do not disable host approvals, weaken tool annotations, bypass operating
   system consent prompts, or attempt to evade an application's safeguards.
7. Use `setup_accessibility` or `setup_window_targeting` only after explaining
   the user-session changes and receiving permission.
