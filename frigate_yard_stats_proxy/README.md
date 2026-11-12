# Frigate Yard Stats Proxy

<img src="icon.png" width="96" align="right" alt="">

Frigate yard activity and vehicle reports, in your Home Assistant sidebar.

The report UI of [Frigate Yard Stats](https://github.com/shuricksumy/frigate-yard-stats)
runs alongside Frigate on its own hardware, and this add-on puts it in the sidebar. Unlike the Music Assistant proxy it does no response rewriting — that service
resolves its own URLs relative to the page, so nothing here is pinned to an upstream
version. See [its docs](DOCS.md).

## Install

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

[![Open your Home Assistant instance and show the dashboard of an add-on.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?addon=frigate_yard_stats_proxy&repository_url=https%3A%2F%2Fgithub.com%2Fshuricksumy%2Fhome-assistant-apps)

1. **Add repository** with the first button (or *Settings → Add-ons → Add-on Store
   → ⋮ → Repositories*).
2. **Open the add-on** with the second button, then *Install*.
3. Set `server_host` and `server_port` to the Yard Stats service, *Start*, and enable *Show in sidebar*.

## Options

| Option | Default | What it is |
| :-- | :-- | :-- |
| `server_host` | `192.168.1.20` | Address of the Yard Stats service. |
| `server_port` | `8080` | Its port. |
| `api_key` | _(empty)_ | Optional. Seeds the UI's API key so you are not asked for it. See [the docs](DOCS.md). |

## License

MIT — see [LICENSE](../LICENSE).
