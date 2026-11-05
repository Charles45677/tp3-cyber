FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py dbHandler.py tasks.db ./

CMD ["python", "api.py"]