FROM corecanarias/docker-ubuntu

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get -yq install mysql-server python-mysqldb

VOLUME  ["/etc/mysql", "/var/lib/mysql"]

ADD run.sh /run.sh
RUN chmod 755 /run.sh

EXPOSE 3306
CMD ["/run.sh"]
