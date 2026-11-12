ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.11@sha256:79fd58d9d7f2820e8b2e7d2b11a24e22b96ae7a48569af3372183592a1b22974
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
    io.hass.name="Music Assistant Proxy" \
    io.hass.description="Music Assistant running on its own hardware, in your Home Assistant sidebar" \
    io.hass.type="addon"
