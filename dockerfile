FROM python:3.11-slim

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the environment variable to recognize the app as a package
ENV PYTHONPATH=/app
CMD sh -c "python -m app.seed_database && uvicorn app.main:app --host 0.0.0.0 --port 8000"
