ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.11@sha256:79fd58d9d7f2820e8b2e7d2b11a24e22b96ae7a48569af3372183592a1b22974
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    nginx \
    gettext

COPY rootfs /

# Required, not redundant: these are tracked without the executable bit, and s6
# silently ignores a service script it cannot execute.
RUN chmod a+x /etc/services.d/nginx/run \
    && chmod a+x /etc/services.d/nginx/finish

LABEL \
    io.hass.name="Frigate Yard Stats Proxy" \
    io.hass.description="Frigate yard activity and vehicle reports, in your Home Assistant sidebar" \
    io.hass.type="addon"
