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
| `ma_token`    | Optional long-lived token for auto-login, see below                 |

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

### Being asked to log in on every visit

Music Assistant binds a saved token to a *connection identity* built from the URL you
reached it on (`local:{protocol}//{host}{path}`). It only restores the token when that
binding matches. Both of the frontend's login paths call `setToken()` without an
identity, which clears the binding, and the re-bind that follows does not survive behind
a proxied ingress — so the token is in your browser but never accepted, and you get the
login screen every time.

Setting `ma_token` fixes this. The proxy injects a small script into the page that writes
the token and a freshly computed matching identity into local storage on every load. The
identity is computed the same way the frontend does, so it stays correct even if the
ingress path changes.

To get a token: in Music Assistant, open your profile settings and create a **long-lived
token**, then paste it into `ma_token` and restart the add-on.

Two caches sit in front of this and both are handled:

- MA serves the index with `ETag`/`Last-Modified`, so a returning browser gets a
  `304` with an empty body. There is nothing there to inject into, so the proxy
  strips the conditional request headers and marks the page `no-store`.
- MA's frontend registers a **service worker** that precaches the app shell, which
  would answer navigations from Cache Storage without ever reaching this proxy.
  While auto-login is on, the proxy replaces `/sw.js` with a worker that
  unregisters itself, handing navigation back to the network. It does not clear
  Cache Storage, because under ingress that is shared with Home Assistant's own
  frontend. Offline support for the panel is lost, which does not apply to an
  ingress panel anyway; visiting the server directly is unaffected.

### One login per address

Tokens are stored per browser origin. Reaching Home Assistant on more than one
address — say `http://192.168.1.2:8123` on the LAN and `https://ha.example.com`
from outside — means a separate login for each. Auto-login covers both, since the
identity is recomputed from whatever address served the page.

> **Note on access.** A seeded token logs everyone who opens the panel in as that user.
> Anyone reaching it already has a Home Assistant login, but if you share Home Assistant
> with people who should not have full Music Assistant control, either leave `ma_token`
> empty or set `"panel_admin": true` in the add-on config so only administrators see it.

## Support

Please open an issue if you need support.
