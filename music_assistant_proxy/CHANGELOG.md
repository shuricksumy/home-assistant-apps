# Changelog

## 1.9.0

- `server_host` now accepts a full URL, not just a host. `https://` upstreams are
  supported, with SNI and the correct Host header so a name-based reverse proxy can
  route them. Previously a URL produced an invalid config and nginx refused to start.
- Bad configuration now pauses before exiting, so the error stays readable instead of
  scrolling past in a restart loop.

## 1.8.0 - 1.8.3

- The panel is restricted to administrators by default.
- Documented what signing in involves: it is a password rather than a token, the
  session lives in browser storage, and it lasts 30 days renewing on use.
- Documented publishing Music Assistant over HTTPS so the "Sign in with Home
  Assistant" button works from an HTTPS address. Players are unaffected by this;
  they are served from a separate address.

## 1.7.0 - 1.7.1

- Fixed a crash caused by the previous release. The replacement service worker
  unregistered itself, but the app waits on `serviceWorker.ready` before opening its
  API connection. It now stays registered with no fetch handler.
- Assets moved to a renamed prefix rather than a query string, so the entry chunk is
  no longer loaded twice under two identities.
- Removed unused files and corrected documentation that described the wrong cause.

## 1.6.0

- Work around Music Assistant deciding it is a Home Assistant add-on purely from the
  URL containing `/hassio_ingress/`. It then authenticates through ingress headers,
  never reads a stored token, and never falls back to the login form, so a proxied
  server dead-ended on "Failed to authenticate via Home Assistant Ingress".

## 1.5.0

- Get past two caches that prevented the page rewrites from reaching the browser: a
  `304` with no body to rewrite, and the service worker answering navigations from
  Cache Storage.

## 1.4.0

- The access token is checked against the server at startup and the result logged, so
  a bad token reports itself instead of silently showing a login screen.
- Whitespace is stripped from a pasted token, which otherwise invalidates it invisibly.
- The generated nginx config is validated before starting.

## 1.3.0

- Optional auto-login via `ma_token`.

## 1.2.0

- Reworked as an Ingress-only proxy. Dropped host networking and the exposed port.
- Fixed configuration changes never taking effect: the nginx template was rendered
  over itself, so after the first boot it held literal values and later edits were
  ignored until reinstall.
- Raised proxy timeouts above the websocket heartbeat to stop idle disconnects.
- Restricted architectures to those the base image actually publishes.
