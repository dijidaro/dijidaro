# Grab the latest alpine image.
FROM python:3.10

WORKDIR /user/src/app

COPY ./requirements.txt .

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    apt-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configure and activate virtual environment.
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/


# Install dependencies.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -q -r requirements.txt

COPY /app .

# Defines environment variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=True

CMD ["python", "app.py"]
