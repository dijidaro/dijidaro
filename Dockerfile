#Grab the latest alpine image
FROM python:3.10

WORKDIR /user/src/app

COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -q -r ./requirements.txt

COPY ./app .

CMD ["python", "app.py"]
