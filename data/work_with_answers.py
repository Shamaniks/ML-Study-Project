from pathlib import Path

# Папка с данными
DATA_DIR = Path(__file__).parent / "answers" # текущая папка, где лежит скрипт

def add_file(filename: str, content: str):
    """Создать новый файл или перезаписать существующий"""
    file_path = DATA_DIR / filename
    if file_path.resolve() == Path(__file__).resolve():
        raise ValueError("Нельзя изменять этот скрипт")
    file_path.write_text(content, encoding="utf-8")

def update_file(filename: str, new_content: str):
    """Перезаписать существующий файл"""
    file_path = DATA_DIR / filename
    if file_path.resolve() == Path(__file__).resolve():
        raise ValueError("Нельзя изменять этот скрипт")
    if not file_path.exists():
        raise FileNotFoundError(f"{filename} не существует")
    file_path.write_text(new_content, encoding="utf-8")

def delete_file(filename: str):
    """Удалить файл"""
    file_path = DATA_DIR / filename
    if file_path.resolve() == Path(__file__).resolve():
        raise ValueError("Нельзя удалять этот скрипт")
    if file_path.exists():
        file_path.unlink()
