# Choosing an image for you container.
FROM python:3.11.0
# This command would copy EVERY FILE from your project folder into your container, so be careful.
COPY telegram_bot.py /app/telegram_bot.py
# Installing needed packages and dependencies.**
RUN pip install -r requirements.txt
# set work directory
WORKDIR /app
# Setting a port for your app communications with Telegram servers.
EXPOSE 80/udp
# This command basically executes your main file with Python.
ENTRYPOINT ["python", "./telegram_bot.py"]
