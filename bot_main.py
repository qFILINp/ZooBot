import asyncio
from aiogram import Bot, Dispatcher, types
from quiz import router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import (Bold, as_list, as_marked_section)
from token_data import TOKEN
from Contact import Mail, Mesag

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
@dp.message(lambda message: message.text.lower() == "вернуться к началу")
async def command_start_handler(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Тест"),
        ],
        [
            types.KeyboardButton(text="Описание бота"),
            types.KeyboardButton(text="Связаться с нами"),
        ],
        [
            types.KeyboardButton(text="О программе опеки"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Приветствую тебя в боте викторине от Московского зоопарка", reply_markup=keyboard)


@dp.message(lambda message: message.text.lower() == "связаться с нами")
async def commands(message: types.Message):
    response = as_list(
        as_marked_section(
            Bold("Вы можете написать нам в соц сетях"),
            f"({Mesag})"))
    response += "\n"
    response += f"Или напишите нам на почту: ({Mail})"
    await message.answer(**response.as_kwargs())


@dp.message(lambda message: message.text.lower() == "описание бота")
async def description(message: types.Message):
    await message.answer("Этот телеграм-бот, позволяет вам пройти небольшую тест на тему какое ваще татемное животное")


@dp.message(lambda message: message.text.lower() == "о программе опеки")
async def command_opiek(message: types.Message):
    await message.answer("Ознакомьтесь с программой опеки по ссылке:")
    await bot.send_message(message.chat.id, "http://moscowzoo.center/")

@dp.message(lambda message: message.text.lower() == "тест")
async def description(message: types.Message):
    kb = [[types.KeyboardButton(text="Начать")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Этот тест позволит узнать какое ваше тотемное животное", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
