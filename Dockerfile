FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install FreeCAD dependencies and Python
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    curl \
    git \
    python3 \
    python3-pip \
    libgl1 \
    libxrender1 \
    libsm6 \
    libxext6 \
    freecad \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Expose FastAPI port
EXPOSE 10000

# Start FastAPI app via uvicorn (for Render)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
