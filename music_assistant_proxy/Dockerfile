ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.10@sha256:e3624401ddd4941b20bf0273d3a1b3d4a0d9061f4034fa3e4722bcc38c8bb4b2
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
