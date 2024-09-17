FROM python:3.12

WORKDIR /Backend

COPY Backend/.env /config/.env

COPY Backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./Backend /Backend

# Expose port 8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
