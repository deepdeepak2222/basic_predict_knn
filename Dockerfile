FROM python:3.9-slim

 # Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

 # Set the working directory
 WORKDIR /apps/recsys

 # Copy the application files
COPY app.py /apps/recsys
COPY requirements.txt /apps/recsys

 # Upgrade pip
 RUN pip install --upgrade pip

 # Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt