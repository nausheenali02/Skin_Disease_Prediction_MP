# Use official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for OpenCV/Pillow
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Hugging Face uses
EXPOSE 7860

# Run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]