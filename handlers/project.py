from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_menu

router = Router()


@router.message(F.text == "📂 Проект")
async def project_menu(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        """
📂 CAM ASSISTANT

Добро пожаловать в менеджер проектов.

Здесь вы сможете:

📦 Создавать проект

📏 Задавать заготовку

🧱 Выбирать материал

📍 Выбирать систему координат

🛠 Добавлять операции

📄 Генерировать один G-код

Функция находится в разработке.
""",
        reply_markup=main_menu,
    )