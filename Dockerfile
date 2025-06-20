# Use official slim Python image
FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Chromium, ChromeDriver, and required libraries
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgtk-3-0 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libx11-6 \
    libdrm2 \
    libxshmfence1 \
    libxcb1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libexpat1 \
    libpq-dev \
    gcc \
    python3-dev \
    fonts-liberation \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Run your script
CMD ["python", "get_data.py"]
