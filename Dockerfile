# Use the official Python image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first (this helps cache dependencies if unchanged)
COPY Backend/requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Install the spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the backend code to the container
COPY Backend/ /app

# Expose port 8000 to the host
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
