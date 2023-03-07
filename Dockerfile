FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get -y install cron vim

# Copying the crontab file 
COPY crontab /etc/cron.d/crontab

# Copy the each file from docker_py_project to py_cronjob in docker container

# run the crontab file

# Executing crontab command

COPY . /app/
# COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
# RUN touch /tmp/out.log
# CMD crond && tail -f /tmp/out.log
# CMD ["python", "main.py"]