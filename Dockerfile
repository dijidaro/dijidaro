# Grab the latest alpine image.
FROM python:3.10

WORKDIR /user/src/app

# Configure and activate virtual environment.
RUN python3 -m venv venv
ENV PATH="/user/src/app/venv/bin:$PATH"

COPY ./requirements.txt .

# Install dependencies.
RUN pip install --no-cache-dir -q -r ./requirements.txt

COPY ./app .

CMD ["python", "app.py"]
