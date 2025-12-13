from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import Model
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
from tensorflow.keras.layers import Input, Dot, Lambda

# Размерность эмбеддингов (для paraphrase-multilingual-MiniLM-L12-v2 это 384)
embedding_dim = 384

# Входы для вопроса и ответа
question_input = Input(shape=(embedding_dim,), name='question')
answer_input = Input(shape=(embedding_dim,), name='answer')

# Косинусное сходство
def cosine_similarity(vects):
    x, y = vects
    x = tf.nn.l2_normalize(x, axis=1)
    y = tf.nn.l2_normalize(y, axis=1)
    return tf.reduce_sum(x * y, axis=1, keepdims=True)

# Слой для вычисления сходства
similarity = Lambda(cosine_similarity)([question_input, answer_input])

# Собираем модель
model = Model(inputs=[question_input, answer_input], outputs=similarity)
model.compile(optimizer='adam', loss='mse')
#model = load_model("saved_similarity_model.keras")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def find_best_answer(question_embedding, answer_embeddings, answers, threshold=0.5):
    similarities = []
    for answer_embedding in answer_embeddings:
        similarity = model.predict([np.array([question_embedding]), np.array([answer_embedding])])[0][0]
        similarities.append(similarity)

    # Находим индекс ответа с максимальным сходством
    best_idx = np.argmax(similarities)
    best_similarity = similarities[best_idx]

    # Если сходство выше порога — возвращаем ответ
    if best_similarity > threshold:
        return answers[best_idx], best_similarity
    else:
        return None, best_similarity


def ask(question: str, answer_embeddings, answers):
    # Получаем эмбеддинг для нового вопроса
    question_embedding = embedding_model.encode([question])[0]

    # Ищем лучший ответ
    best_answer, similarity = find_best_answer(question_embedding, answer_embeddings, answers=answers)
    if best_answer:
        return best_answer, round(similarity, 2)
    else:
        return 'Ответ не найден (сходство слишком низкое).', round(similarity, 2)

# --- Тестовая часть, которую потом нужно будет убрать ---

answers = [
    "Map-Reduce — это модель обработки больших данных, состоящая из двух этапов: map (преобразование данных) и reduce (агрегация результатов).",
    "Spark — это фреймворк для распределённой обработки данных, поддерживающий SQL, машинное обучение и потоковую обработку.",
    "Hadoop — это экосистема для хранения и обработки больших данных, включающая HDFS (распределённая файловая система) и YARN (менеджер ресурсов).",
    "Kafka — это распределённая платформа для потоковой передачи данных, часто используемая для реального времени и логирования.",
    "SQL — это язык запросов для работы с реляционными базами данных, поддерживающий операции SELECT, INSERT, UPDATE и DELETE."
]
answer_embeddings = embedding_model.encode(answers)

q = input('Введте вопрос: ')
b_a, s = ask(q, answer_embeddings, answers)
print(b_a, s)

