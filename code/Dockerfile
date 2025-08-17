FROM python:3.11-slim

WORKDIR /app

# Copy the Python script into container
COPY app.py .

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    libfreetype6-dev \
    libxft-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required packages
RUN pip install --no-cache-dir \
yfinance \
pandas \
matplotlib \
openpyxl

# Set environment variable to avoid matplotlib GUI issues
ENV MPLBACKEND=Agg

# Create output and charts directories
RUN mkdir -p /app/output /app/charts

CMD ["python", "app.py"]