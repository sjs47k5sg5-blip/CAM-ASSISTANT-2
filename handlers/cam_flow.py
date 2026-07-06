from aiogram import Router, F
from aiogram.types import Message

from handlers.cam_state import CAM_DB, CamState

router = Router()


# =========================
# STATE
# =========================
def state(uid: int) -> CamState:
    if uid not in CAM_DB:
        CAM_DB[uid] = CamState()
    return CAM_DB[uid]


# =========================
# MILLING ENTRY
# =========================
@router.message(F.text == "⚙ Фрезерная обработка")
async def milling(message: Message):
    await message.answer("⚙ ФРЕЗЕРОВКА\n\n📐 Контур\n📦 Карман\n📏 Обводка")


# =========================
# CONTOUR MAIN SCREEN (FIXED UI)
# =========================
@router.message(F.text == "📐 Контур")
async def contour(message: Message):

    u = state(message.from_user.id)
    u.step = 1

    from keyboards.cam_menu import params_menu

    await message.answer(
        "📐 КОНТУР CAM\n\n"
        "⚙ Введите параметры обработки ниже 👇",
        reply_markup=params_menu()
    )


# =========================
# SIZE INPUT
# =========================
@router.message(F.text == "📏 Размер детали")
async def size(message: Message):
    await message.answer("Введите X Y Z (пример: 30 30 30)")


@router.message(F.text.regexp(r"^\d+ \d+ \d+$"))
async def size_set(message: Message):

    u = state(message.from_user.id)

    x, y, z = message.text.split()

    u.x = float(x)
    u.y = float(x)
    u.z = float(z)

    await message.answer("✔ Размер сохранён")


# =========================
# MATERIAL
# =========================
@router.message(F.text == "🧱 Материал")
async def material(message: Message):
    await message.answer("ALU / STEEL / BRASS / COPPER")


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
# ZERO Z
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
# CORNERS
# =========================
@router.message(F.text == "⚙ Обработка углов")
async def corners(message: Message):
    await message.answer("Все / ЛВ / ЛН / ПВ / ПН")


@router.message(F.text.in_(["Все","ЛВ","ЛН","ПВ","ПН"]))
async def corners_set(message: Message):
    u = state(message.from_user.id)
    u.corner_target = message.text
    await message.answer("радиус / фаска / острые")


@router.message(F.text.in_(["радиус","фаска","острые"]))
async def corner_type(message: Message):
    u = state(message.from_user.id)
    u.corner_mode = message.text.upper()
    await message.answer("Введите значение (мм)")


@router.message(F.text.regexp(r"^\d+(\.\d+)?$"))
async def corner_value(message: Message):
    u = state(message.from_user.id)
    u.corner_value = float(message.text)
    await message.answer("✔ углы настроены")


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
    await message.answer("Готово → нажмите ГЕНЕРАЦИЯ")


# =========================
# GENERATE
# =========================
@router.message(F.text == "ГЕНЕРАЦИЯ")
async def generate(message: Message):

    u = state(message.from_user.id)

    from services.cam_engine import contour

    gcode = contour(
        x=u.x,
        y=u.y,
        depth=u.z,
        stepdown=2,
        tool=u.tool_d,
        zero=u.zero,
        allowance=0.2,
        step=0,
        corner_type=u.corner_mode,
        corner_value=u.corner_value
    )

    await message.answer(f"<pre>{gcode}</pre>", parse_mode="HTML")