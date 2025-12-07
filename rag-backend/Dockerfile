FROM python:3.11-slim

WORKDIR /app

# Install system dependencies that might be needed for certain packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]