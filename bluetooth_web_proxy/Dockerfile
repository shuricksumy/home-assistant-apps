ARG BUILD_FROM=ghcr.io/hassio-addons/base:20.0.2
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    nginx \
    gettext \
    curl

COPY rootfs /

# Required, not redundant: these are tracked without the executable bit, and s6
# silently ignores a service script it cannot execute.
RUN chmod a+x /etc/services.d/nginx/run \
    && chmod a+x /etc/services.d/nginx/finish

LABEL \
    io.hass.name="Bluetooth Web Snapclient Proxy" \
    io.hass.description="Pair Bluetooth speakers and run Snapcast players on another machine, from your Home Assistant sidebar" \
    io.hass.type="addon"
