import asyncio
from app import build
from config.settings import TOKEN

def main():
    application = build(TOKEN)
    application.run_polling()

if __name__ == "__main__":
    main()
