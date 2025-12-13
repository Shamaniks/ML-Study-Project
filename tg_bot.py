import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from token import token


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

with open("TOKEN.txt", "r") as file:
    content = file.read()
TOKEN = token
SERVER_URL = "..."




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я - бот, который поможет разобраться Вам в программировании. Введите ваш вопрос.')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    print(user_message)

    # Отправляем сообщение на сервер
    # try:
    #     response = requests.post(SERVER_URL, json={"message": user_message})
    #     response.raise_for_status()
    #     server_response = response.json().get("answer", "Сервер не вернул ответ.")
    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Ошибка при отправке на сервер: {e}")
    #     server_response = "Не удалось связаться с сервером."
    #
    # Отправляем ответ пользователю
    server_response = user_message.upper()
    await update.message.reply_text(server_response)

def main():
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()



if __name__ == '__main__':
    main()