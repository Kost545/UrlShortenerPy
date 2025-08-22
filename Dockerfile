FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]