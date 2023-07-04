FROM ubuntu:latest

LABEL authors="Adam"

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libxext6\
    libxrender1\
    libgl1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY app/requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the application code
COPY app/ .

# Set the entrypoint to execute main.py
ENTRYPOINT ["python3", "main.py"]
