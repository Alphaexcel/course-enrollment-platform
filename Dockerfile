# Use official Python 3.11 slim image
FROM python:3.11-slim


# Set working directory inside container
WORKDIR /app


# Copy requirements first (for better caching)
COPY requirements.txt .


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of your project
COPY . .


# Expose port 8000
EXPOSE 8000


# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
