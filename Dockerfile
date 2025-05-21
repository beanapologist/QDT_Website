FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install numpy and scipy first (they take longer)
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    scipy==1.10.1 \
    --only-binary :all:

# Copy requirements and install other dependencies
COPY requirements.txt .
RUN grep -v "numpy\|scipy" requirements.txt > other_requirements.txt && \
    pip install --no-cache-dir -r other_requirements.txt

# Copy source code and package files
COPY src/ src/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install the package in development mode
RUN pip install -e .

# Set environment variables
ENV FLASK_APP=src.api.crystal_calculator_api
ENV FLASK_ENV=development
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"] 