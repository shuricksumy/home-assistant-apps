ARG BUILD_FROM=ghcr.io/hassio-addons/base:20.0.2
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
    io.hass.description="Ingress proxy to a Frigate Yard Stats report UI running elsewhere" \
    io.hass.type="addon"
