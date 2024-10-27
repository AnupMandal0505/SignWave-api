# Use the official Python image from the Docker Hub
FROM python:3.11

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Run migrations (optional)
# RUN python manage.py migrate

# Collect static files (optional)
# RUN python manage.py collectstatic --noinput

# Expose the port the app runs on (default is 8000)
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver"]
