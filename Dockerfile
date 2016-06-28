FROM ubuntu:latest
MAINTAINER Markus Heider "markus@heiders.net"
RUN apt-get update -y && \
			apt-get install -y \
			build-essential \
			python-pip \
			python-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

