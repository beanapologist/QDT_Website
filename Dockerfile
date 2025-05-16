# Use multi-stage build for optimized image size
FROM python:3.10.12-slim-bullseye AS backend

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    gfortran \
    python3-dev \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install scientific packages separately with specific platform tags
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    scipy==1.10.1 \
    --only-binary=:all:

# Copy requirements first for better caching
COPY requirements.txt .

# Install remaining requirements
RUN grep -v "numpy\|scipy" requirements.txt > other_requirements.txt && \
    pip install --no-cache-dir -r other_requirements.txt && \
    rm other_requirements.txt

# Copy backend code
COPY src/ src/
COPY setup.py .
COPY README.md .
COPY LICENSE .

# Install the package
RUN pip install -e .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src/api/crystal_calculator_api.py
ENV FLASK_ENV=production

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]

# Frontend build stage
FROM node:18 AS frontend-build

WORKDIR /app

# Copy package.json first
COPY package.json ./

# Install dependencies
RUN npm install

# Copy configuration files
COPY tsconfig.json ./

# Copy frontend source
COPY src/ src/
COPY public/ public/

# Build frontend
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy frontend build
COPY --from=frontend-build /app/build /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 