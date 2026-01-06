FROM python:3.13-slim

WORKDIR /app

COPY ../docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../app/ .

EXPOSE 8550

CMD ["python", "main.py"]