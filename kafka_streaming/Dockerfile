FROM jedha/confluent-image

RUN apt-get update
RUN apt-get -y install gcc

COPY requirements.txt .

RUN pip install -r requirements.txt
