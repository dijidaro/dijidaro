# Grab the latest alpine image.
FROM python:3.10

WORKDIR /user/src/app

COPY ./requirements.txt .

# Configure and activate virtual environment.
RUN python3 -m venv /venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies.
RUN pip install --no-cache-dir -q -r requirements.txt

COPY /app .

# Defines environment variables
ENV FLASK_APP=app.py

CMD ["python", "app.py"]
