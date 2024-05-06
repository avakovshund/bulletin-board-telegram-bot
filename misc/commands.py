from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.admin_panel.admin_filter import my_admin_list

# Menu button that helps to work with bot and shows available commands for different user types (default user and admin)
async def set_commands(bot: Bot):
    await bot.set_my_commands(
            commands=[
                BotCommand(command="/start", description="Start work and restart bot."),
                BotCommand(command="/help", description="Rules and explanation.")
                ],
            scope=BotCommandScopeDefault()
            )
    for admins in my_admin_list:
        await bot.set_my_commands(
            commands=[
                BotCommand(command="/start", description="Start work and restart bot."),
                BotCommand(command="/help", description="Rules and explanation."),
                BotCommand(command="/admin", description="Admin panel."),
                BotCommand(command="/image", description="Change/set welcome image.")
                ],
            scope=BotCommandScopeChat(chat_id=admins)
            )