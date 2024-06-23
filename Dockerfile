# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip
    # pip install -r requirements.txt
    # pip install fastapi uvicorn openai pymongo python-dotenv motor passlib python-multipart

# Copy the application files to the container
COPY . .

RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]