# Use lightweight Python base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    default-libmysqlclient-dev build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run app with Gunicorn (production server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]


