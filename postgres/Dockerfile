FROM postgres:16
RUN localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8
ENV LANG ru_RU.utf8
RUN apt update && apt install -y postgresql-16-rum postgresql-16-postgis-3 postgresql-16-pgrouting cron nano && apt-get clean