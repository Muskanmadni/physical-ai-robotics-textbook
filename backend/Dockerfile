FROM python:3.11-slim

WORKDIR /app

# Install system dependencies that might be needed for compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main", "--host", "0.0.0.0", "--port", "8000"]