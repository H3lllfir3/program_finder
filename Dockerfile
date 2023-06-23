FROM python:3.9.16-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get -y install cron vim

# Copying the crontab file 
COPY crontab /etc/cron.d/crontab


COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system
COPY . /app/
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

RUN mkdir -p /app/data

RUN python manage.py makemigrations && python manage.py migrate

CMD cron && tail -f /var/log/cron.log
