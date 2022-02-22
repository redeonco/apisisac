FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app/requirements.txt ./app/requirements.txt
COPY ./app/celery.sh ./app/celery.sh
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN apt update && apt install tzdata -y
ENV TZ="America/Sao_Paulo"

ENV ACCEPT_EULA=Y
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
  && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

RUN apt-get update

RUN apt-get update -yqq \
    && apt-get install -y --no-install-recommends openssl \ 
    && sed -i 's,^\(MinProtocol[ ]*=\).*,\1'TLSv1.0',g' /etc/ssl/openssl.cnf \
    && sed -i 's,^\(CipherString[ ]*=\).*,\1'DEFAULT@SECLEVEL=1',g' /etc/ssl/openssl.cnf\
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
      && apt-get install -y redis-server
EXPOSE 6379

RUN apt-get install -y zabbix-agent

COPY ./zabbix_agentd.conf /etc/zabbix

RUN service zabbix-agent restart

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get install -y unixodbc && \
    /py/bin/pip install -r requirements.txt && \
    /py/bin/pip install django-celery-beat && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 775 /vol && \
    chmod -R 755 /vol/web/static && \
    chmod -R +x /scripts && \
    chmod -R 664 /app/celery.sh

RUN pip install uwsgi

ENV PATH="/scripts:/py/bin:$PATH"

USER app

COPY ./app .

CMD ["celery.sh"]
