ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.1.0@sha256:ce73287a53cc08874e5fa8e3fe3e9aac098171c40326c0d384e93a5761e067b2
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
