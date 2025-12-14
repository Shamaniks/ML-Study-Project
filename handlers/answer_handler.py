from similarity import load_answers_and_embeddings, ask, embedding_model

# Загружаем ответы и эмбеддинги один раз
answers, answer_embeddings = load_answers_and_embeddings()

async def handle_user_message_model(event, application):
    best_answer, similarity = ask(
        question=event.text,
        answers=answers,
        answer_embeddings=answer_embeddings
    )

    reply = best_answer if best_answer else "Ответ не найден"
    await application.bot.send_message(
        chat_id=event.chat_id,
        text=reply
    )
