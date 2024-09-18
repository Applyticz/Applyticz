FROM python:3.12

WORKDIR /app

# Only copy requirements first to install dependencies (this layer can be cached)
COPY Backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Expose port 8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
