import asyncio
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from collections import Counter
from dict import questions, photo, name
from token_data import TOKEN
from URL_Gen import generate_vk_share_url


class VikStage(StatesGroup):
    quiz = State()
    end = State()


bot = Bot(token=TOKEN)

event = asyncio.Event()
router = Router()
last_message_id = None


@router.message(lambda message: message.text.lower() in ["начать", "пройти тест снова"])
async def send_question(message: types.Message, state: FSMContext):
    questions_list = questions['questions']

    for i, q in enumerate(questions_list):
        question_text = q['quest']
        answers = q['answ']
        await state.update_data({f'question_{i + 1}': answers})

        builder = ReplyKeyboardBuilder()
        for answer_key, data in answers.items():
            builder.add(types.KeyboardButton(text=f"{answer_key}"))
        builder.adjust(1)

        await message.answer(f"{question_text}", reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(VikStage.quiz)
        await event.wait()
        event.clear()

    await state.set_state(VikStage.end)

    end_button = ReplyKeyboardBuilder()
    end_button.add(types.KeyboardButton(text="Покажи результат"))
    await message.answer("Это был последний вопрос. Хотите увидеть результат?",
                         reply_markup=end_button.as_markup(resize_keyboard=True))


@router.message(VikStage.quiz)
async def but_cl(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_question = await state.get_state()
    key = message.text.lower()

    found = False
    for question_key, answers in data.items():
        if question_key.startswith("question_") and current_question == VikStage.quiz:
            if key in answers:
                await state.update_data({f'{question_key}_{key}': answers[key]})
                found = True
                event.set()

    if not found:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")


@router.message(lambda message: message.text == "Покажи результат")
async def show_most_common_ind(message: types.Message, state: FSMContext):
    data = await state.get_data()
    inds = []
    for key, value in data.items():
        if key.startswith('question_'):
            if isinstance(value, dict):
                for chosen_answer, ind_list in value.items():
                    ind_key = f'{key}_{chosen_answer}'
                    if ind_key in data:
                        inds.extend(data[ind_key])
            else:
                continue

    counts = Counter(inds)
    most_common_inds = [ind for ind, count in counts.items() if count == max(counts.values())]

    result_text = "Твоё тотемное животное настоящий"
    if len(most_common_inds) == 1:
        most_common_ind = most_common_inds[0]
        photo_url = photo['photo'][int(most_common_ind) - 1][most_common_ind]
        name_p = name['name'][int(most_common_ind) - 1][most_common_ind]
        caption = f"{result_text} {name_p}"
    else:
        photo_url = "https://pvtest.ru/wp-content/uploads/b/c/5/bc592a1bdb7c3d64b1412d00cc529d19.png"
        caption = f"{result_text} Невиданный зверь"
    vk_btn = InlineKeyboardButton(text="Поделиться в ВК", url=f"{await generate_vk_share_url(photo_url, caption)}")
    row = [[vk_btn]]
    mark = InlineKeyboardMarkup(inline_keyboard=row)
    kb = [
        [
            types.KeyboardButton(text="О программе опеки"),
        ], [
            types.KeyboardButton(text="Пройти тест снова"),
            types.KeyboardButton(text="Вернуться к началу"),
        ], ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_photo(chat_id=message.chat.id, photo=photo_url,
                         caption=caption, reply_markup=mark)
    await message.answer('Поздравляю с прохожением теста теперь вы можете ознакомиться с программой опеки животных '
                         'или пройти тест снова', reply_markup=keyboard)

    counts.clear()
    await state.clear()
