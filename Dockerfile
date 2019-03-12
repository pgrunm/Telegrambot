# Getting the latest alpine linux image
FROM alpine:latest

# Install necessary packages like Python3 etc
RUN apk --no-cache add python3 \
    python3-dev \
    build-base \
    libffi-dev \
    openssl-dev

# Run the following commands within /app/Telegrambot
WORKDIR /app/Telegrambot

# Copy everything inside /app/Telegrambot except directories and files listed in the .dockerignore file.
COPY * /app/Telegrambot/

# Install the required packages with pip
RUN pip3 install --upgrade pip && \
    pip3 install -r /app/Telegrambot/requirements.txt 

# Save the API key in the environment
ENV tg_api_key=0123456789:ABCqxtafQx-5aYP8U1zRB9oEgXTzZ2Awx1M

CMD ["python3", "/app/Telegrambot/bot.py"]