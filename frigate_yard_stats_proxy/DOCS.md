# Frigate Yard Stats Proxy

This add-on does **not** run Yard Stats. It is an nginx reverse proxy that puts the
report UI of a [Frigate Yard Stats](https://github.com/shuricksumy/frigate-yard-stats)
service running somewhere else into the Home Assistant sidebar via Ingress.

## Requirements

The report UI must resolve its API calls relative to the page it is served from. Older
builds call `/events` and friends as absolute paths, which resolve against Home
Assistant instead of the service and return 404 behind Ingress. If the panel loads
styled but stays empty, that is the symptom — update the service.

## Configuration

| Option        | Description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| `server_host` | Address of the Yard Stats service: an IP, a hostname, or a full URL     |
| `server_port` | Port of its API (default `8080`, matching `API_PORT`)                   |
| `api_key`     | Optional. Seeds the UI's API key so you are not asked for it            |

A hostname is resolved once when nginx starts. If the address changes, restart the
add-on.

## Signing in

The report UI keeps an API key in a cookie and sends it as `X-API-Key` on every call.
By default you paste the key once in the UI and it is remembered.

Setting `api_key` writes it into the page instead, so the panel is usable immediately.

> **Note on access.** A seeded key is written into the page, so anyone who can open the
> panel can read it and use it directly against the service, outside Home Assistant.
> The panel is admin-only by default. Leave `api_key` empty if you would rather each
> person hold their own key.

## How it works

Ingress opens an add-on at its root, but the report UI lives at `/ui/`. The proxy
redirects the root there rather than proxying it, because the page's assets are
relative — the browser has to actually be at `/ui/` for them to resolve. The redirect
target is relative, so it lands inside the Ingress path without this add-on needing to
know what that path is.

Everything else is passed straight through. Unlike the Music Assistant proxy in this
repository, no response rewriting is involved: the service resolves its own URLs
correctly, so there is nothing here pinned to a particular upstream version.

Range requests are passed through so video seeking works, and read timeouts are
generous because clips stream off disk.

## Support

Please open an issue if you need support.
