FROM python:3.10-alpine
ADD ./src /app
ADD ./src/templates /app/templates
WORKDIR /app
RUN pip install -r requirements.txt