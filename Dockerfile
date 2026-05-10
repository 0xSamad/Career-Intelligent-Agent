FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better cache on build
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/

# Expose port (Cloud Run sets PORT env var)
EXPOSE 8080

# Command to run the application
CMD ["python", "src/app.py"]
