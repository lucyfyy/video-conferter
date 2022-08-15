#2022 Mikun copyright
FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["python3", "main.py"]