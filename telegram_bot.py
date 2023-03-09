import os
import requests
import telegram
import asyncio
import time
import datetime as dt
from dotenv import load_dotenv

load_dotenv()


VK_TOKEN = os.getenv("VK_TOKEN")
USER1_ID = os.getenv("VK_USER1_ID")
USER2_ID = os.getenv("VK_USER2_ID")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def get_vk_status(user_id):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_id': user_id,
        'fields': 'online',
        'v': '5.92',
        'access_token': VK_TOKEN
    }
    response = requests.post(url, params=params).json()['response']

    return response[0] # Верните статус пользователя в ВК


async def send_message(message):
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    users = [
        {'id': USER1_ID, 'previous_status': 0},
        {'id': USER2_ID, 'previous_status': 0},
    ]

    while True:
        try:
            for user in users:
                status = get_vk_status(user['id'])
                if status['online'] == 1:
                    if user['previous_status'] == 0:
                        timer = dt.datetime.now().strftime('%H:%M %d.%m.%Y')
                        msg = f'{status["first_name"]} {status["last_name"]} сейчас онлайн! {timer}'
                        asyncio.run(send_message(msg))
                user['previous_status'] = status['online']
            time.sleep(60)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()

