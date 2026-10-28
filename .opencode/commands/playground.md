---
description: Start the Sloperator playground on a port, reusing an already-running server
---

# Playground

Requested port: $ARGUMENTS

Resolve the port before doing anything else: if the value above is empty, use
`8080`. It must be a number.

## Current TCP listeners

!`lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null`

## Check before starting

Inspect the listener list above. A Sloperator server is a `uv`/Python process
whose command line contains `playground/server.py`; a socket alone may belong to
an unrelated program. Use `ps -p <PID> -o command=` when the command name is not
enough.

1. **Sloperator already serving the resolved port** — reuse it. Do not start a
   second server. Confirm it responds on that port.
2. **A different program owns the port** — stop and report the owner. Do not
   kill it or silently pick another port.
3. **Port is free** — start the server in the background from the project root:

   ```bash
   uv run playground/server.py <port>
   ```

   Substitute the resolved port (never `$ARGUMENTS` inside a shell block). Run it
   with nohup/background so the session stays usable, capture its PID and log,
   then wait until the port is listening and the page responds.

## Report

State the injected listener list, the resolved port, which case applied, the
server PID (when there is one), and the playground URL. On reuse, make clear
that no new process was started. Leave the server running.
