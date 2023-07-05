FROM python:3.11-alpine

WORKDIR /user/src/app

# Set up environment variable.
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

# Install dependencies.
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

# Run app.
CMD ["flask" ,"run"]
