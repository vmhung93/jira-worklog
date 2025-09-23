# Stage 1: Builder
# Use a full Python image on Alpine for building and installing dependencies
FROM python:3.12-alpine AS builder

# Set the working directory
WORKDIR /app

# Install build dependencies required by many Python packages
RUN apk add --no-cache gcc musl-dev

# Copy the requirements file
COPY requirements.txt .

# Install dependencies. This will create the uvicorn executable.
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Copy only the installed packages from the builder stage's site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the uvicorn executable from the builder stage
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy your application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]