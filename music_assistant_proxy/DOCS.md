# Music Assistant Proxy

This add-on does **not** run Music Assistant. It is an nginx reverse proxy that puts a
Music Assistant server running somewhere else (Docker, another machine) into the Home
Assistant sidebar via Ingress.

## Why this works

Music Assistant's frontend is built with relative asset paths (`./assets/...`) and a
hash-based router, and it derives its websocket URL from `window.location.pathname`.
That makes it safe to serve from a sub-path, which is exactly what Ingress does
(`/api/hassio_ingress/<token>/`). Home Assistant strips that prefix before forwarding
and passes the original in the `X-Ingress-Path` header, so a plain `proxy_pass` is
enough — no HTML rewriting required.

## Configuration

| Option        | Description                                                        |
| ------------- | ------------------------------------------------------------------ |
| `server_host` | IP or hostname of the Music Assistant server (e.g. `192.168.1.10`) |
| `server_port` | Port of the Music Assistant web interface (default `8095`)          |
| `ma_token`    | Optional bearer token, see the note on authentication below         |

A hostname is resolved once when nginx starts. If your server's IP changes, restart the
add-on.

## Authentication

Music Assistant 2.6+ has its own authentication, and a proxied server cannot bypass it.
When MA runs as a Home Assistant add-on it trusts the `X-Remote-User-*` headers, but only
on a dedicated socket bound to the internal Docker bridge (`172.30.32.x:8094`), verified
at the socket level rather than by header. A remote server never sees that socket, so
that path is closed by design.

In practice: open the panel and log in once with MA's built-in username/password. The
session is stored in the browser against your Home Assistant origin and persists, so this
is a one-time step. Note that this session is separate from any session you have when
visiting the server directly on its own address.

`ma_token` sets an `Authorization: Bearer` header on proxied HTTP requests. The web UI
authenticates in-band over the websocket, so this does **not** skip the login screen —
it only covers direct HTTP API calls made through the proxy. Leave it empty unless you
need that.

## Support

Please open an issue if you need support.
