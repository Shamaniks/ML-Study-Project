from similarity import load_answers_and_embeddings, ask, embedding_model

# Загружаем ответы и их эмбеддинги один раз при старте приложения
answers, answer_embeddings = load_answers_and_embeddings()


async def handle_user_message_model(event, application):
    """
    Обрабатывает сообщение пользователя с помощью модели сходства:
    получает наиболее подходящий ответ и отправляет его в чат.
    """

    # Получаем лучший ответ и степень сходства из нейросети
    best_answer, similarity = ask(
        question=event.text,
        answers=answers,
        answer_embeddings=answer_embeddings
    )

    # Если модель не уверена или ответ не найден — возвращаем fallback-сообщение
    reply = best_answer if best_answer else "Ответ не найден"

    # Отправляем ответ пользователю
    await application.bot.send_message(
        chat_id=event.chat_id,
        text=reply
    )
