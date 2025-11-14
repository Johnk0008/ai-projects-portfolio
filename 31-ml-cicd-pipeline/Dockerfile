# Use Python 3.9
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY *.py ./

# Create necessary directories
RUN mkdir -p templates static

# Copy templates and static files
COPY app/templates/ ./templates/
COPY app/static/ ./static/

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.main
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]