# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Create a non-root user to run the app
RUN useradd -m -u 1000 user

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the image
COPY --chown=user:user requirements.txt /app

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY --chown=user:user . /app

# Expose the port the app runs on
EXPOSE 7860

# Change to the non-root user
USER user

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
