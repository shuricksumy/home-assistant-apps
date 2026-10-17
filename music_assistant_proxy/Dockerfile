ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.8@sha256:52f79347fa3e0ceb58af92aecca8165c34099067dde8c5f767e95d9cdd56099f
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
