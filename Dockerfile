FROM python:3.8-slim-buster

ARG SERVICEBUS_CONNECTION_STR
ARG SERVICEBUS_TOPIC_NAME
ARG SERVICEBUS_TOPIC_NAME

ENV SERVICEBUS_CONNECTION_STR=${SERVICEBUS_CONNECTION_STR}
ENV SERVICEBUS_TOPIC_NAME=${SERVICEBUS_TOPIC_NAME}
ENV SERVICEBUS_SUBSCRIPTION_NAME=${SERVICEBUS_SUBSCRIPTION_NAME}

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python3" , "src/app.py"]
