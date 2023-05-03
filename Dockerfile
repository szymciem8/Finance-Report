FROM python:3.11
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/code
COPY requirements.txt ./
RUN pip install -r requirements.txt