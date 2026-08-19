# Bluetooth Web Snapclient Proxy

Puts [bluetooth-web-snapclient](https://github.com/shuricksumy/bluetooth-web-snapclient)
into your Home Assistant sidebar when it runs on a different machine.

## Configuration

```yaml
server_host: 192.168.1.50
server_port: 8088
username: admin
password: your-admin-password
```

### server_host

Where the panel runs. Accepts a bare host (`192.168.1.50`), a host with a port
(`192.168.1.50:8088`), or a full URL (`https://panel.example.lan:443`) if it is
already published through a reverse proxy.

A port in `server_host` wins over `server_port`. A URL *without* a port does not
fall back to the scheme default — `https://panel.lan` with `server_port: 8088`
means `panel.lan:8088`, not 443. Spell the port out when it matters.

### server_port

The panel's port. Default `8088`, matching its compose example.

### username / password

The panel's `ADMIN_USER` and `ADMIN_PASSWORD`. The proxy sends them upstream on
every request so the sidebar does not prompt you a second time — Ingress has
already authenticated you against Home Assistant.

Leave `password` empty if the panel runs with no auth. That is only reasonable on
a trusted LAN, and this add-on does not change that: it reaches the panel over
your network exactly as a browser would.

## What it does not do

- It does not run Bluetooth or Snapcast itself. Add-ons cannot bind arbitrary host
  paths, so the PipeWire socket the players need is out of reach; and Home
  Assistant OS runs no PipeWire session at all. The panel stays on the machine
  with the audio hardware, and this add-on shows it to you.
- It does not proxy album art. Those URLs point at Music Assistant, and the
  browser fetches them directly.
