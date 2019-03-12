# Telegrambot

Just a small project for my personal convenience.

- Parses the free ebook of the day and sends it with URL to claim to you.
- Ability to send a German joke when mentioned inline (made it for my GF ;))
- maybe some more Features to be added. ;-)

## Deployment in a Container

Now there is a Dockerfile added, so you deploy this bot easily in a container. Just do the following:

1. Change the API key inside the Dockerfile to your API key.
2. Create and run the container with the following lines:

    ```Dockerfile
    # Building the image from the docker file in the current directory
    docker build --rm -f "Dockerfile" -t Warryz_Telegram_Bot:latest .

    # And now run the container
    docker --rm run Warryz_Telegram_Bot:latest
    ````
