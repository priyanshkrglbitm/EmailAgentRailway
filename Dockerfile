# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port if needed (only for web apps, optional)
# EXPOSE 8080

# Run your app
CMD ["python", "app.py"]
