from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState
from keyboards.cam_menu import milling_menu, params_menu, corner_menu, finish_menu

router = Router()


def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# ENTRY MILLING
# =========================
@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):
    await message.answer("Выберите операцию", reply_markup=milling_menu())


# =========================
# CONTOUR
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):
    u = state(message.from_user.id)
    u.step = 1
    await message.answer("Введите параметры", reply_markup=params_menu())


# =========================
# SIZE INPUT
# =========================
@router.message(F.text == "📏 Размеры детали")
async def size(message: Message):
    await message.answer("Введите X Y Z (например 30 30 30)")


@router.message(F.text.regexp(r"^\d+ \d+ \d+$"))
async def size_input(message: Message):
    u = state(message.from_user.id)

    if u.step != 1:
        return

    x, y, z = message.text.split()
    u.x, u.y, u.z = float(x), float(y), float(z)

    await message.answer("✔ Размер сохранён")


# =========================
# MATERIAL
# =========================
@router.message(F.text == "🧱 Материал")
async def material(message: Message):
    await message.answer("ALU / STEEL / BRASS / COPPER (пока текстом)")

@router.message(F.text.in_(["ALU","STEEL","BRASS","COPPER"]))
async def material_set(message: Message):
    u = state(message.from_user.id)
    u.material = message.text
    await message.answer("✔ Материал выбран")


# =========================
# ZERO
# =========================
@router.message(F.text == "📍 Ноль детали")
async def zero(message: Message):
    await message.answer("CENTER / TL / TR / BL / BR")

@router.message(F.text.in_(["CENTER","TL","TR","BL","BR"]))
async def zero_set(message: Message):
    u = state(message.from_user.id)
    u.zero = message.text
    await message.answer("✔ Ноль установлен")


# =========================
# Z ZERO
# =========================
@router.message(F.text == "📍 Ноль Z")
async def zeroz(message: Message):
    await message.answer("TOP / BOTTOM")

@router.message(F.text.in_(["TOP","BOTTOM"]))
async def zeroz_set(message: Message):
    u = state(message.from_user.id)
    u.zero_z = message.text
    await message.answer("✔ Z установлен")


# =========================
# CORNER MODE
# =========================
@router.message(F.text == "⚙ Обработка углов")
async def corner(message: Message):
    await message.answer("Выберите тип", reply_markup=corner_menu())


@router.message(F.text.in_(["Все","ЛВ","ЛН","ПВ","ПН"]))
async def corner_target(message: Message):
    u = state(message.from_user.id)
    u.corner_target = message.text
    await message.answer("Введите тип угла: фаска / радиус / острые")


@router.message(F.text.in_(["ФАС","РАД","ОСТ"]))
async def corner_mode(message: Message):
    u = state(message.from_user.id)
    u.corner_mode = message.text
    await message.answer("Введите значение (мм)")


@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def corner_value(message: Message):
    u = state(message.from_user.id)
    u.corner_value = float(message.text)
    await message.answer("✔ угол настроен")


# =========================
# ALLOWANCE
# =========================
@router.message(F.text == "📉 Припуск")
async def allowance(message: Message):
    await message.answer("0 / 0.2 / 0.5")

@router.message(F.text.in_(["0","0.2","0.5"]))
async def allowance_set(message: Message):
    u = state(message.from_user.id)
    u.allowance = float(message.text)

    if u.allowance != 0:
        u.finish_pass = "YES"
    await message.answer("✔ припуск установлен")


# =========================
# TOOL
# =========================
@router.message(F.text == "🔧 Инструмент")
async def tool(message: Message):
    await message.answer("Введите диаметр")


@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def tool_set(message: Message):
    u = state(message.from_user.id)
    u.tool_d = float(message.text)
    await message.answer("✔ инструмент установлен")


# =========================
# READY
# =========================
@router.message(F.text == "✅ Готово")
async def ready(message: Message):
    await message.answer("Готово → нажмите ГЕНЕРАЦИЯ", reply_markup=finish_menu())


# =========================
# GENERATION (ENGINE CONNECT)
# =========================
@router.message(F.text == "ГЕНЕРАЦИЯ")
async def gen(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=u.x,
        y=u.y,
        depth=u.z,
        stepdown=2,
        tool=u.tool_d,
        zero=u.zero,
        allowance=u.allowance,
        step=0,
        corner_type=u.corner_mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")