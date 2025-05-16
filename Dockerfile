# Use multi-stage build for optimized image size
FROM python:3.10-bullseye AS backend

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

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY requirements.txt .

# Install numpy first separately
RUN pip install --no-cache-dir numpy==1.24.3

# Then install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

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