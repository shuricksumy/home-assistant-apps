# Music Assistant Proxy

This add-on does **not** run Music Assistant. It is an nginx reverse proxy that puts a
Music Assistant server running somewhere else (Docker, another machine) into the Home
Assistant sidebar via Ingress.

## Configuration

| Option        | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `server_host` | IP or hostname of the Music Assistant server (e.g. `192.168.1.10`) |
| `server_port` | Port of the Music Assistant web interface (default `8095`)           |
| `ma_token`    | Optional long-lived token for auto-login, see below                  |

A hostname is resolved once when nginx starts. If your server's IP changes, restart the
add-on.

## Signing in

Music Assistant 2.6+ has its own authentication and a proxied server cannot bypass it.
When MA runs as a real add-on it trusts `X-Remote-User-*` headers, but only on a socket
bound to the internal Docker bridge (`172.30.32.x:8094`), verified at socket level rather
than by header. A remote server never binds that port, so that path is closed by design.

So: open the panel and sign in once with your Music Assistant username and password. The
session is kept, so it is a one-time step.

### Auto-login

Set `ma_token` to skip the sign-in entirely. In Music Assistant, open your profile
settings, create a **long-lived token**, paste it into `ma_token`, and restart the
add-on. The proxy writes it into the page on every load.

The add-on checks the token against the server at startup and says so in its log, so a
bad token reports itself instead of silently showing a login screen:

```
Token accepted by Music Assistant, seeding the web UI session
Music Assistant rejected the token (HTTP 401). Create a fresh long-lived token...
Could not reach Music Assistant at <host>:<port> to verify the token.
```

> **Note on access.** A seeded token signs in everyone who opens the panel as that user.
> Anyone reaching it already has a Home Assistant login, but if you share Home Assistant
> with people who should not have full Music Assistant control, either leave `ma_token`
> empty or set `"panel_admin": true` in the add-on config so only administrators see it.

### One login per address

Sessions are stored per browser origin. Reaching Home Assistant on more than one address
— say `http://192.168.1.2:8123` on the LAN and `https://ha.example.com` from outside
— means signing in separately on each. Auto-login covers both, since it is recomputed
from whatever address served the page.

## What the proxy rewrites, and why

Music Assistant's frontend uses relative asset paths and a hash router, so it is happy
being served from a sub-path like `/api/hassio_ingress/<token>/`. That part needs no
help. Three things do.

**It thinks it is an add-on.** MA decides it is running as a Home Assistant add-on purely
from the URL containing `/hassio_ingress/`. Having decided that, it authenticates through
ingress headers, never reads a stored token, and deliberately never falls back to the
login form — so a proxied server dead-ends on *"Failed to authenticate via Home Assistant
Ingress"*. The proxy rewrites that check to `false` as the bundle is served, which puts
the normal login and token path back in reach.

**Assets are served under a renamed prefix.** MA sends no `Cache-Control` on assets, only
a validator, so a browser holding the un-rewritten bundle would revalidate into a `304`
and keep using it. Renaming the directory rather than adding a query string keeps every
module in one URL namespace, so nothing is loaded twice under two identities.

**The service worker is replaced.** MA's own worker precaches the app shell and would
answer navigations from Cache Storage without ever reaching this proxy. The replacement
registers and claims normally but installs no fetch handler, so requests reach the
network. It stays registered on purpose — the app awaits `serviceWorker.ready` with no
timeout before opening its API connection — and it does not clear Cache Storage, which
under ingress is shared with Home Assistant's own frontend.

One visible side effect: MA no longer treats the panel as an ingress session, so the small
Home Assistant back button inside the panel is gone. Use the sidebar.

### Compatibility

These rewrites are keyed to details of the currently released Music Assistant build. The
underlying bug is fixed upstream by frontend #2216, *"Fix login behind Home Assistant
ingress"*, which no released server build carries yet. Once one does, the ingress-check
rewrite should be deleted rather than maintained.

If a future MA update changes the bundle, the rewrites stop matching and quietly do
nothing — the symptom is the old *"Failed to authenticate via Home Assistant Ingress"*
error returning.

## Support

Please open an issue if you need support.
