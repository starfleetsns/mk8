FROM python:3.5.3-jessie
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["/app/start.sh"]
