import os
from dotenv import load_dotenv

load_dotenv()

from aiogram.filters import BaseFilter
from aiogram.types import Message

# Admin ID check filter
admins = os.getenv('ADMINS')
my_admin_list = admins.split(',')

class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in my_admin_list