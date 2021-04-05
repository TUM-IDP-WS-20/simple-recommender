FROM nginx:1.19

# Cleanup the default configuration files
RUN rm -f /etc/nginx/nginx.conf \
    && rm -rf /etc/nginx/conf.d/ \
    && mkdir -p /etc/nginx/conf.d

# Copy our custom files
COPY nginx.conf /etc/nginx/
COPY api.vh.conf /etc/nginx/conf.d/
