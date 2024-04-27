# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the backend directory contents into the container at /app/backend
COPY ./backend /app/backend

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Change the working directory to /app/backend where the Flask app is
WORKDIR /app/backend

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
