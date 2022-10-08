FROM python:alpine3.16
WORKDIR /project
COPY ./src ./src
COPY ./requirements.txt .
RUN pip install -r requirements.txt