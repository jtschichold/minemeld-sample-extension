FROM minemeld:test
COPY . /tmp
RUN cp /tmp/docker/committed-config.yml /opt/minemeld/local/config/
RUN /opt/minemeld/engine/current/bin/pip3 install /tmp
