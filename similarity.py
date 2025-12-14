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

# Размерность векторного представления (эмбеддинга)
embedding_dim = 384

# Функция для вычисления косинусного сходства между двумя векторами
def cosine_similarity(vects):
    x, y = vects
    # Нормализация векторов по L2, чтобы косинусное сходство было корректным
    x = tf.nn.l2_normalize(x, axis=1)
    y = tf.nn.l2_normalize(y, axis=1)
    # Возвращаем косинусное сходство
    return tf.reduce_sum(x * y, axis=1, keepdims=True)

# Входные слои для модели: векторы вопроса и ответа
question_input = Input(shape=(embedding_dim,), name='question')
answer_input = Input(shape=(embedding_dim,), name='answer')

# Lambda слой для вычисления сходства между векторами
similarity = Lambda(cosine_similarity)([question_input, answer_input])

# Создаем модель, которая на вход принимает пару векторов и возвращает их сходство
model = Model(inputs=[question_input, answer_input], outputs=similarity)

# Компилируем модель с оптимизатором Adam и функцией потерь MSE
model.compile(optimizer='adam', loss='mse')


# --- Логика поиска лучшего ответа ---
def find_best_answer(question_embedding, answer_embeddings, answers, threshold=0.5):
    """
    Находит наиболее подходящий ответ на основе косинусного сходства эмбеддингов.

    Параметры:
    - question_embedding (np.array или tf.Tensor): эмбеддинг вопроса
    - answer_embeddings (list of np.array или tf.Tensor): эмбеддинги возможных ответов
    - answers (list of str): список текстовых ответов
    - threshold (float): минимальное значение сходства, при котором ответ считается подходящим

    Возвращает:
    - best_answer (str или None): наиболее подходящий ответ (или None, если сходство ниже порога)
    - best_similarity (float): максимальное косинусное сходство
    """

    # Список для хранения сходств вопроса с каждым ответом
    similarities = []

    # Вычисляем сходство каждого ответа с вопросом
    for answer_embedding in answer_embeddings:
        # model.predict ожидает батч данных, поэтому оборачиваем в np.array и добавляем размерность [1, ...]
        similarity = model.predict([np.array([question_embedding]), np.array([answer_embedding])])[0][0]
        similarities.append(similarity)

    # Находим индекс ответа с максимальным сходством
    best_idx = np.argmax(similarities)
    best_similarity = similarities[best_idx]

    # Проверяем, превышает ли максимальное сходство заданный порог
    if best_similarity > threshold:
        return answers[best_idx], best_similarity  # возвращаем лучший ответ и его сходство

    # Если подходящего ответа нет, возвращаем None и максимальное сходство
    return None, best_similarity


def ask(question: str, answers, answer_embeddings):
    """
    Находит наиболее подходящий ответ на заданный вопрос.

    Параметры:
    - question (str): вопрос, на который ищем ответ
    - answers (list of str): список возможных ответов
    - answer_embeddings (list of np.array или tf.Tensor): заранее вычисленные эмбеддинги ответов

    Возвращает:
    - best_answer (str или None): наиболее подходящий ответ
    - similarity (float): косинусное сходство вопроса и выбранного ответа (округлено до 2 знаков)
    """

    # Получаем эмбеддинг для заданного вопроса
    question_embedding = embedding_model.encode([question])[0]

    # Ищем лучший ответ среди списка, используя эмбеддинги
    best_answer, similarity = find_best_answer(question_embedding, answer_embeddings, answers)

    # Если найден подходящий ответ, возвращаем его и схожесть
    if best_answer:
        return best_answer, round(similarity, 2)
    else:
        # Если подходящего ответа нет, возвращаем None и схожесть
        return None, round(similarity, 2)
