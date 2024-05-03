# Use the official Python 3.6 image as base image
FROM python:3.6

# Set up a non-root user
RUN useradd -ms /bin/bash nonroot

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change ownership of the application directory to the non-root user
RUN chown -R nonroot /app

# Switch to the non-root user
USER nonroot

# Expose the port on which your Flask app will run
EXPOSE 5001

# Command to run the Flask application CMD ["python3", "/app/run.py"]
CMD ["python3", "/app/run.py"]
