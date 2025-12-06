FROM python:3.11-slim

# Avoid Python buffering issues in logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (app + tests)
COPY . .

# Expose container port
EXPOSE 8000

# Default command for running the app in a container
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
