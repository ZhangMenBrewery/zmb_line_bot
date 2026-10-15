FROM python:3.13-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD [ "gunicorn", "zmb_line_bot.wsgi:application", "--bind", "0.0.0.0:8000" ]
