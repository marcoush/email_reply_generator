FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir gradio pandas requests

COPY app.py .
COPY past_emails.csv .

EXPOSE 7860

CMD ["python", "app.py"]