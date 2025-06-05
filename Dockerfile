FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

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
    && add-apt-repository ppa:freecad-maintainers/freecad-stable -y \
    && apt-get update && apt-get install -y freecad \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

EXPOSE 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
