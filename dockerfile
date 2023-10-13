FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip & pip install -r requirements

COPY . /app/

CMD [ "gunicorn", "zmb_line_bot.wsgi:application", "--bind", "0.0.0.0:8000" ]