FROM python:3.9-slim

WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining project files
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the chatbot API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]