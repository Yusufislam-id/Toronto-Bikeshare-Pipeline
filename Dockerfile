FROM python:3.12

WORKDIR /app
COPY requirements.txt requirements.txt
COPY upload-data.py download-data.py

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" , "download-data.py" ]