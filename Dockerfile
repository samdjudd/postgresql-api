FROM python:3.7-slim

RUN apt-get update
RUN apt-get install postgresql-client -y
RUN apt-get install curl -y
ARG mode
ENV MODE=$mode
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
