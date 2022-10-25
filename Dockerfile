FROM python:3.10-alpine
ADD ./src /app
WORKDIR /app
RUN pip install -r requirements.txt