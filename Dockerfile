# Use the official Python 3.10 image (Stable for TensorFlow)
FROM python:3.10

# Hugging Face requires running as a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the Docker image
COPY --chown=user . .

# Hugging Face exposes port 7860 by default
EXPOSE 7860

# Command to start the FastAPI server on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]