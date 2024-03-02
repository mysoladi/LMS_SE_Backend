# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /lms_login_api

# Copy the current directory contents into the container at /app
COPY . /lms_login_api

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 3000

# Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]