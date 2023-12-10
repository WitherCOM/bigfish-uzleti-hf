FROM docker.io/alpine:3.17
COPY ./overlay/ /
RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev python3-dev nginx nginx-mod-http-headers-more python3 py3-pip && \
	pip3 install --no-cache-dir -r /app/requirements.txt && \
	apk del gcc libressl-dev musl-dev libffi-dev python3-dev
WORKDIR /app
EXPOSE 80


ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
