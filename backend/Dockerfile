# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Make port 9090 available to the world outside this container
EXPOSE 9090

# Run main.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
