# Step 1: Use official Python base image
FROM python:3.9-slim

# Step 2: Set environment variables to avoid writing .pyc files and enable buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy requirements.txt file (if present) for dependency installation
COPY requirements.txt /app/

# Step 5: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the entire app to the working directory
COPY . /app/

# Step 7: Expose port 8080 for the Flask application
EXPOSE 8080

# Step 8: Set environment variables for MySQL connection (optional, these can also be set in a docker-compose.yml file)
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=password
ENV MYSQL_HOST=mysql
ENV MYSQL_DATABASE=testdb

# Step 9: Command to run the Flask application
CMD ["python", "app.py"]