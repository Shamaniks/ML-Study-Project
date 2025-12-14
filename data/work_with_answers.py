from pathlib import Path

# Директория answers, расположенная рядом с текущим скриптом
ANSWERS_DIR = Path(__file__).parent / "answers"


def _check_path(filename: str):
    """
    Внутренняя функция проверки безопасности пути.

    Гарантирует, что работа ведётся только с файлами внутри папки answers
    (защита от path traversal: ../, абсолютных путей и т.п.)
    """
    file_path = ANSWERS_DIR / filename
    file_path = file_path.resolve()  # приводим к абсолютному пути

    # Проверяем, что файл действительно находится внутри ANSWERS_DIR
    if not str(file_path).startswith(str(ANSWERS_DIR.resolve())):
        raise ValueError("Файл должен находиться внутри папки answers")

    return file_path


def select_files(pattern: str):
    """
    Возвращает список файлов из папки answers,
    имя которых содержит указанную подстроку pattern.
    """
    return [f.name for f in ANSWERS_DIR.iterdir() if pattern in f.name]


def add_file(filename: str, content: str):
    """
    Создаёт новый файл в папке answers или перезаписывает существующий.

    Параметры:
    - filename (str): имя файла
    - content (str): содержимое файла
    """
    file_path = _check_path(filename)
    file_path.write_text(content, encoding="utf-8")


def update_file(filename: str, new_content: str):
    """
    Обновляет содержимое существующего файла.

    Вызывает ошибку, если файл не найден.
    """
    file_path = _check_path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"{filename} не существует")

    file_path.write_text(new_content, encoding="utf-8")


def delete_file(filename: str):
    """
    Удаляет файл из папки answers, если он существует.
    """
    file_path = _check_path(filename)

    if file_path.exists():
        file_path.unlink()
