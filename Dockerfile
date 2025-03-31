# Wolf-tcp-server Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY tcpserver.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tcpserver.py"]