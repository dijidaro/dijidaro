# Grab the latest alpine image.
FROM python:3.10

WORKDIR /user/src/app

COPY ./requirements.txt .

# Configure and activate virtual environment.
RUN python3 -m venv /venv
ENV PATH="/app/venv/bin:$PATH"

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    && apt-get clean

ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"

# Install dependencies.
RUN pip install --no-cache-dir -q -r requirements.txt

COPY /app .

# Defines environment variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=True
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

CMD ["python", "app.py"]
