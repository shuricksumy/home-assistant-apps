# Changelog

## 1.0.0

- First release. Proxies bluetooth-web-snapclient through Home Assistant Ingress.
- `server_host` accepts a bare host, `host:port`, or a full URL.
- Optional `username`/`password` are sent upstream as Basic auth so the sidebar
  does not ask for credentials a second time.
- The add-on log reports on every start whether the panel answered, and says
  which option to check when it did not.
