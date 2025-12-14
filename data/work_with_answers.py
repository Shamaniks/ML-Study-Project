from pathlib import Path

# Папка с данными
ANSWERS_DIR = Path(__file__).parent / "answers" # текущая папка, где лежит скрипт

def _check_path(filename: str):
    """Внутренняя проверка: файл должен быть в answers и не сам скрипт"""
    file_path = ANSWERS_DIR / filename
    file_path = file_path.resolve()  # абсолютный путь
    if not str(file_path).startswith(str(ANSWERS_DIR.resolve())):
        raise ValueError("Файл должен быть внутри папки answers")
    return file_path

def add_file(filename: str, content: str):
    """Создать новый файл или перезаписать существующий"""
    file_path = _check_path(filename)
    file_path.write_text(content, encoding="utf-8")

def update_file(filename: str, new_content: str):
    """Перезаписать существующий файл"""
    file_path = _check_path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"{filename} не существует")
    file_path.write_text(new_content, encoding="utf-8")

def delete_file(filename: str):
    """Удалить файл"""
    file_path = _check_path(filename)
    if file_path.exists():
        file_path.unlink()
