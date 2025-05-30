FROM python:3.11

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
    libssl-dev \
    libmariadb-dev \
    mariadb-client

WORKDIR /app/backend
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ../backend/tiny-link/api /app/backend/tiny-link/api 
COPY ../backend/tiny-link/manage.py /app/backend/tiny-link
COPY ../backend/tiny-link/tinyLink /app/backend/tiny-link/tinyLink

COPY --chmod=0755 ../docker/start.sh /
ENV PYTHONUNBUFFERED=1
WORKDIR /
CMD [ "/bin/bash" ]
