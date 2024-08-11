FROM --platform=amd64 python:3.12-slim-bullseye
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY ./duty_bot /app

USER root
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD [ "python3", "__main__.py" ]
