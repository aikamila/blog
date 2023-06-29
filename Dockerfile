# Use an official Python runtime as the base image
FROM python:3.9
 
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY entrypoint.sh /entrypoint.sh
# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the current directory contents into the container at /app
COPY . .
 
# Expose port 8000 for the Django development server
EXPOSE 8000

RUN chmod +x /entrypoint.sh
# Define the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


