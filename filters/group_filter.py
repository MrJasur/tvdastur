from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class isGroup(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        return msg.chat.type in(
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )