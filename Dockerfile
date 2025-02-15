FROM python:3.9

COPY data /app/data
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY data_ingestion.py data_ingestion.py

ENTRYPOINT [ "python" , "data_ingestion.py" ]