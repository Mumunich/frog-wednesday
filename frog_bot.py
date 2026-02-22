import asyncio
import os
import requests
import httpx
from aiogram import Bot

# Секреты из GitHub Actions
TOKEN = os.getenv("BOT_TOKEN")
FRIEND_ID = os.getenv("FRIEND_ID", "").split(",")
# Прямая ссылка на картинку в репозитории
BACKUP_FROG = "https://github.com/Mumunich/movie-watchlist-bot/raw/main/qVGFmwd7WlfeNIOvGLXMMKxUXLlMJkiM6eTDepyKnCrd57jNe5DCrBrLQU6e_QywJtrVxGntV9YyQaPo_XuKGlyr.jpg"

def check_api_status():
    """Пример использования REQUESTS (синхронно)"""
    url = "https://onlypepes.com"
    try:
        # Requests удобен для быстрых проверок 'в одну строку'
        r = requests.head(url, timeout=5)
        return r.status_code == 200
    except:
        return False


async def get_pepe_url():
    url = "https://onlypepes.com/api/pepe?limit=1&random=true"
    # 1. Сначала проверим статус через requests (просто для шпаргалки)
    if not check_api_status():
        return BACKUP_FROG

    # 2. А теперь тянем данные через httpx (основной путь)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                pepe_link = data.get("data", {}).get("url")
                if pepe_link:
                    return pepe_link
        except Exception as e:
            print(f"❌ Ошибка HTTPX: {e}")

    return BACKUP_FROG


async def send_pepe():
    pepe_url = get_pepe_url()
    bot = Bot(token=TOKEN)
    text = "Лямгущька поздравляет тебя со средой, мой дорогой друг! 🐸"

    for user_id in FRIEND_ID:
        user_id = user_id.strip()  # Убираем лишние пробелы
        if not user_id: continue

        try:
            await bot.send_photo(chat_id=user_id, photo=pepe_url, caption=text)
            print(f"✅ Пепе отправлен пользователю {user_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки для {user_id}: {e}")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(send_pepe())