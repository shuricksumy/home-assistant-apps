# Changelog

## 1.0.1

- Force relative redirects, so nothing can send the browser to this container's own
  address instead of back through Ingress.

## 1.0.0

- First release. Proxies a Frigate Yard Stats report UI into the Home Assistant
  sidebar via Ingress.
- Optional `api_key` seeding, so the UI does not ask for a key.
- `server_host` accepts a bare host, a `host:port`, or a full URL including `https://`.
