from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .menu import render_menu


async def show_main_menu(
    target: Message | CallbackQuery,
    state: FSMContext,
):

    text, kb = await render_menu(state)

    if isinstance(target, CallbackQuery):

        try:

            await target.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=kb
            )

        except TelegramBadRequest:

            await target.message.answer(
                text,
                parse_mode="HTML",
                reply_markup=kb
            )

        await target.answer()

        return

    await target.answer(
        text,
        parse_mode="HTML",
        reply_markup=kb
    )