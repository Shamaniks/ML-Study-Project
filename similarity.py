# similarity.py
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Lambda

# Путь к папке с файлами
ANSWERS_DIR = "data/answers"
CACHE_FILE = "data/answers_cache.pkl"

embedding_dim = 384
# Загружаем модель
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def load_answers_and_embeddings():
    """
    Загружает ответы из файлов и их эмбеддинги.
    Если есть кэш — загружает кэш, иначе считает и сохраняет.
    """
    # 1 Проверка кэша
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            data = pickle.load(f)
            answers = data["answers"]
            embeddings = data["embeddings"]
            print("Загружены ответы и эмбеддинги из кэша.")
            return answers, embeddings

    # 2 Если кэша нет — читаем файлы
    answers = []
    for filename in sorted(os.listdir(ANSWERS_DIR)):
        if filename.endswith(".txt"):
            path = os.path.join(ANSWERS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                answers.append(text)

    # 3 Вычисляем эмбеддинги
    embeddings = embedding_model.encode(answers)

    # 4 Сохраняем в кэш
    with open(CACHE_FILE, "wb") as f:
        pickle.dump({"answers": answers, "embeddings": embeddings}, f)

    print(f"Загружено {len(answers)} ответов, эмбеддинги сохранены в кэш.")
    return answers, embeddings

def cosine_similarity(vects):
    x, y = vects
    x = tf.nn.l2_normalize(x, axis=1)
    y = tf.nn.l2_normalize(y, axis=1)
    return tf.reduce_sum(x * y, axis=1, keepdims=True)

question_input = Input(shape=(embedding_dim,), name='question')
answer_input = Input(shape=(embedding_dim,), name='answer')

# Слой для вычисления сходства
similarity = Lambda(cosine_similarity)([question_input, answer_input])

# Собираем модель
model = Model(inputs=[question_input, answer_input], outputs=similarity)
model.compile(optimizer='adam', loss='mse')

# --- Логика поиска ---
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

def ask(question: str, answers, answer_embeddings):
    question_embedding = embedding_model.encode([question])[0]
    best_answer, similarity = find_best_answer(question_embedding, answer_embeddings, answers)
    if best_answer:
        return best_answer, round(similarity, 2)
    else:
        return None, round(similarity, 2)
