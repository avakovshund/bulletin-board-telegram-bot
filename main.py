import asyncio
import logging
import betterlogging
import os
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.middleware.db_middleware import DataBaseSession
from app.database.engine import create_db, session_maker
from app.database.scheduled_func import check_for_date
from app.user_panel.user_routers import user_router
from app.admin_panel.admin_routers import admin_router
from misc.commands import set_commands

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')

dp = Dispatcher()

scheduler = AsyncIOScheduler()

# Creating DB and adding scheduled job that checks every day for out timed ads
async def on_startup():
    await create_db()
    
    scheduler.add_job(check_for_date, 'cron', args=[session_maker()], hour='23', minute='00')
    scheduler.start()
    
    await set_commands(bot)

# Main function
async def main():
    betterlogging.basic_colorized_config(level=logging.INFO) # You can remove it before release
    
    await on_startup()
    
    dp.include_routers(user_router, admin_router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Try/except to start bot and ignore KeyboardInterrupt error
try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.info("Bot stopped!")