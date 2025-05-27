# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all test code into container
COPY . .

# Run only the specific test file
CMD ["pytest", "Tests/test_login.py", "--alluredir=allure-results"]

# COPY test_login.py /app/test_login.py
