# Use the official Python 3.12.0-slim image as the base image
FROM python:3.12.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirments.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirments.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the FastAPI app's default port (you can change it if needed)
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
