FROM python:3.11

WORKDIR /app/backend

COPY requirements.txt .
COPY ./scripts/setup.sh /app/scripts/setup.sh
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/scripts/setup.sh && /app/scripts/setup.sh
COPY . .

ENV PYTHONUNBUFFERED=1
