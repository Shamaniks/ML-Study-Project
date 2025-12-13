import asyncio
from app import build, setup_background_tasks
from config.settings import TOKEN

async def main():
    application = build(TOKEN)
    setup_background_tasks(application)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
