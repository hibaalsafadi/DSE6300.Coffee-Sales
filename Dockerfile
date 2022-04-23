FROM python:3.7-slim

WORKDIR /opt/application/

RUN apt-get update
RUN apt-get install default-jdk -y

ADD https://jdbc.postgresql.org/download/postgresql-42.2.5.jar /opt/spark/jars

RUN pip install --no-cache-dir matplotlib pandas numpy pyspark kafka-python

COPY main.py ./
COPY transactionAnalysis.py ./

CMD [ "python", "./main.py"]