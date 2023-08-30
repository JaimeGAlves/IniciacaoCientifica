# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install openbabel dependency
RUN apt-get update && apt-get install -y openbabel

# Create a virtual environment and install Python dependencies
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

# Expose the port the app runs on (adjust as needed)
EXPOSE 8000

# Run the command to start the API using Uvicorn
CMD ["venv/bin/uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
