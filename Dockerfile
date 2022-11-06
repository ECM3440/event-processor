FROM python:3.8-slim-buster

ARG SERVICEBUS_CONNECTION_STR
ARG SERVICEBUS_SENSOR_TOPIC
ARG SERVICEBUS_ACTUATOR_TOPIC
ARG SERVICEBUS_SUBSCRIPTION_NAME

ENV SERVICEBUS_CONNECTION_STR=${SERVICEBUS_CONNECTION_STR}
ENV SERVICEBUS_SENSOR_TOPIC=${SERVICEBUS_SENSOR_TOPIC}
ENV SERVICEBUS_ACTUATOR_TOPIC=${SERVICEBUS_ACTUATOR_TOPIC}
ENV SERVICEBUS_SUBSCRIPTION_NAME=${SERVICEBUS_SUBSCRIPTION_NAME}

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app
RUN pip3 install pytest pytest-cov mock pytest-httpserver
RUN python -m pytest --cov-config=.coveragerc --cov=. --cov-branch --exitfirst --verbose --failed-first --cov-fail-under=70

RUN rm -rf /app/src/test

EXPOSE 8080
CMD [ "python3" , "src/main/app.py", "--profile", "prod"]
