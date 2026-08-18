# Music Assistant Proxy

This add-on does **not** run Music Assistant. It is an nginx reverse proxy that puts a
Music Assistant server running somewhere else (Docker, another machine) into the Home
Assistant sidebar via Ingress.

## Configuration

| Option        | Description                                                          |
| ------------- | -------------------------------------------------------------------- |
| `server_host` | IP or hostname of the Music Assistant server (e.g. `192.168.1.11`) |
| `server_port` | Port of the Music Assistant web interface (default `8095`)           |
| `ma_token`    | Optional long-lived token for auto-login, see below                  |

A hostname is resolved once when nginx starts. If your server's IP changes, restart the
add-on.

If the server has more than one local address, point `server_host` at the same one Music
Assistant publishes as its base URL (its System settings, visible at
`http://<server>:<port>/info`), so everything leaves through one address.

If that base URL is instead a public hostname — see the HTTPS note under signing in —
keep `server_host` on the direct local address. The proxy reaches Music Assistant over the
local network and should not detour through a public name.

## Signing in

Music Assistant 2.6+ has its own authentication and a proxied server cannot bypass it.
When MA runs as a real add-on it trusts `X-Remote-User-*` headers, but only on a socket
bound to the internal Docker bridge (`172.30.32.x:8094`), verified at socket level rather
than by header. A remote server never binds that port, so that path is closed by design.

So: open the panel and sign in once. If Music Assistant has its Home Assistant login
provider enabled you can use your existing Home Assistant account rather than a separate
Music Assistant password (see the caveat below); otherwise use a Music Assistant username
and password.

The session is then kept, so it is a one-time step. It lives in the browser's local
storage — no cookies are involved — which means:

- **Per browser.** Phone, laptop and desktop each sign in once. Nothing syncs between them.
- **Per address.** Reaching Home Assistant on more than one address means one sign-in each,
  because storage is scoped to the origin.
- **Independent of Home Assistant.** Signing out of Home Assistant does not clear it.

It lasts 30 days and renews on each use, with a hard 90 day cap, so expect to sign in
again about quarterly.

### Signing in with your Home Assistant account

Music Assistant redirects to Home Assistant to authorise, then back again. Both hops have
to stay on the same scheme, and Music Assistant builds those URLs from its own configured
addresses, not from the address you are browsing.

So this works when you reach Home Assistant over plain HTTP on the LAN. Over an HTTPS
address it is blocked as mixed content, because the redirect targets an HTTP URL from an
HTTPS page — unless Music Assistant itself is reachable over HTTPS. A Music Assistant
username and password works on both.

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

> **Note on access.** Leaving `ma_token` empty is the safer default, and is why it ships
> empty. A seeded token is not just an auto-login: it is written into the page, so anyone
> who can open the panel can read it out of the page source and then use it directly
> against the Music Assistant server — outside Home Assistant entirely, past its login and
> past removing that person's Home Assistant account. Signing in individually keeps each
> person's access tied to their own Music Assistant account instead.
>
> The panel is restricted to administrators (`"panel_admin": true`). If you want everyone
> in the household to reach it, set that to `false` — and prefer individual sign-in over a
> shared token when you do, since that widens who could extract it.

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
