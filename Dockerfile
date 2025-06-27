# Use a slim Python image
FROM python:3.11-slim

# Disable .pyc files and buffer flushing
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files into container
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the app
EXPOSE 8000

# Start Gunicorn server using your actual project name
CMD ["gunicorn", "locksmith_picks.wsgi:application", "--bind", "0.0.0.0:8000"]
