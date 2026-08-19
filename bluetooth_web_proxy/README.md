# Bluetooth Web Snapclient Proxy

<img src="icon.png" width="96" align="right" alt="">

Pair Bluetooth speakers and run Snapcast players on **another machine**, from your
Home Assistant sidebar.

[bluetooth-web-snapclient](https://github.com/shuricksumy/bluetooth-web-snapclient)
has to run where the Bluetooth adapter and the PipeWire session are — usually the
box wired to your DAC, not the one running Home Assistant. That leaves it off the
sidebar, because Ingress only serves add-ons. This add-on is the missing half: a
small nginx that proxies it through Ingress, so it appears in Home Assistant with
HA's own authentication in front and works over Nabu Casa like anything else.

## Install

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

[![Open your Home Assistant instance and show the dashboard of an add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=bluetooth_web_proxy&repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

1. **Add repository** with the first button (or *Settings → Add-ons → Add-on Store
   → ⋮ → Repositories*).
2. **Open the add-on** with the second button, then *Install*.
3. Fill in the options below, *Start*, and enable *Show in sidebar*.

## Options

| Option | Default | What it is |
| :-- | :-- | :-- |
| `server_host` | `192.168.1.50` | Where the panel runs. A bare host, `host:port`, or a full URL if it already sits behind a reverse proxy. A URL without a port still uses `server_port`, so give `https://panel.lan:443` explicitly when that is what you mean. |
| `server_port` | `8088` | The panel's port. Ignored when `server_host` already carries one. |
| `username` | `admin` | Matches the panel's `ADMIN_USER`. |
| `password` | _(empty)_ | Matches the panel's `ADMIN_PASSWORD`. Leave empty if the panel runs without auth. |

The password is sent upstream on every request, so you are not asked for it twice:
Ingress has already authenticated you against Home Assistant before anything
reaches the proxy.

## Notes

- **Album art comes from Music Assistant directly.** The browser fetches
  `artUrl` from the MA host, so artwork works on your LAN but will not load from
  outside it. Everything else goes through the proxy.
- **The panel is never exposed.** Only Home Assistant reaches it; the add-on does
  not publish a port of its own.
- **Nothing to patch.** The panel resolves its API calls relative to the document,
  so it lands correctly under Ingress with no response rewriting — unlike the
  Music Assistant proxy in this repo, which has to rewrite an SPA it does not own.

## Troubleshooting

The add-on log says on every start whether the panel answered:

```
Panel reachable at http://192.168.1.50:8088
```

- **`Could not reach …`** — check `server_host`/`server_port`, and that the
  panel's port is published on that machine.
- **`rejected our credentials (HTTP 401)`** — `username`/`password` do not match
  the panel's `ADMIN_USER`/`ADMIN_PASSWORD`.
- **Sidebar page is blank** — the panel is reachable but something upstream is
  failing; open the panel directly on its own host to see its error.
