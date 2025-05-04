# Use NVIDIA CUDA base image for GPU support
FROM nvidia/cuda:12.0.1-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic link for python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
