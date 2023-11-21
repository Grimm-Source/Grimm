FROM python:3.6

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && apt-get install -y mariadb-server-10.5

WORKDIR /app
CMD bash setup_dev/entrypoint.sh
