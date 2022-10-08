FROM python:alpine3.16
WORKDIR /src
COPY /src /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt