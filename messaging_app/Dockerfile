# Use official Python image
FROM python:3.10

# Set work directory
WORKDIR /app

# Install dependencies
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port 8000
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "-p", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
