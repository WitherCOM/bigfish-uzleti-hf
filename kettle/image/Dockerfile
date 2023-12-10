FROM openjdk:22-slim-bookworm

ARG PDI_VERSION=9.4.0.0-343
ARG MARIADB_JDBC_VERSION=3.3.0
RUN apt-get update && apt-get install -y wget unzip fontconfig \
    && wget --progress=dot:giga https://privatefilesbucket-community-edition.s3.us-west-2.amazonaws.com/$PDI_VERSION/ce/client-tools/pdi-ce-$PDI_VERSION.zip \
	&& unzip -q pdi-ce-$PDI_VERSION.zip \
	&& rm -f pdi-ce-${PDI_VERSION}.zip

WORKDIR /data-integration

RUN wget "https://dlm.mariadb.com/3478935/Connectors/java/connector-java-${MARIADB_JDBC_VERSION}/mariadb-java-client-${MARIADB_JDBC_VERSION}.jar" -P lib/

COPY /overlay/ /

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]