# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY ./backend/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY ./backend /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start the Django app
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
