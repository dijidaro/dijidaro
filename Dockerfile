# Official Python image as base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /user/src/app

# Copy requirements.txt file into the container
COPY requirements.txt .

# Configure and activate virtual environment.
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use port 5000
EXPOSE 5000

# Copy the entire application into the container
COPY ./app .

# Defines environment variables
ENV FLASK_APP=app.py

# Run the flask app
CMD ["python", "app.py"]