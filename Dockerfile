# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and any other dependencies
RUN pip install --no-cache-dir flask

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]