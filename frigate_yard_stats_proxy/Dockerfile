ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.9@sha256:f0067c8e469c86f0ccd019ba79657d56827671ef49430aadc16ce27190426036
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
