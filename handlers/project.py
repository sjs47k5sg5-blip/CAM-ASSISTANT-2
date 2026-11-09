from __future__ import annotations

import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Document, InlineKeyboardButton, InlineKeyboardMarkup, Message

from services.cam_engine.project_geometry import parse_dxf, parse_manual_path
from services.cam_engine.geometry_validation import build_rounded_polygon, validate_geometry
from services.cam_engine.geometry_preview import render_geometry_preview
from services.cam_engine.geometry_offset import offset_geometry
from services.cam_engine.profile_toolpath import build_profile_toolpath, render_toolpath_preview
from services.cam_engine.project_store import add_operation, create_project, get_project, list_projects, set_geometry

router = Router()


class ProjectWizard(StatesGroup):
    name = State()
    stock = State()
    manual_geometry = State()
    rounded_polygon = State()
    offset_tool = State()
    profile_diameter = State()
    profile_depth = State()
    profile_stepdown = State()
    profile_side = State()
    profile_allowance = State()


def kb(rows):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=label, callback_data=data) for label, data in row]
        for row in rows
    ])


def project_summary(project):
    stock = project["stock"]
    return (f"<b>🗂 {project['name']}</b>\nЗаготовка: {stock['x']:g} × {stock['y']:g} × {stock['z']:g} мм\n"
            f"Геометрия: {'задана' if project['geometry'] else 'не задана'}\nОпераций: {len(project['operations'])}")


def project_kb():
    return kb([
        [("📐 DXF", "proj:dxf"), ("✍️ Линии/дуги", "proj:manual")],
        [("🔘 Скруглённый контур", "proj:rounded")],
        [("👁 Предпросмотр", "proj:preview")],
        [("🧰 Проверить смещение фрезы", "proj:offset")],
        [("🛤 Траектория контура", "proj:toolpath")],
        [("➕ Добавить контур", "proj:add:contour"), ("➕ Добавить карман", "proj:add:pocket")],
        [("📋 Операции", "proj:ops"), ("⬅ Проекты", "proj:list")],
    ])


@router.message(F.text == "🗂 Проект")
async def project_menu(message: Message, state: FSMContext):
    await state.clear()
    projects = list_projects(message.from_user.id)
    rows = [[(f"📁 {p['name']}", f"proj:open:{p['id']}")] for p in projects[:10]]
    rows.append([("➕ Новый проект", "proj:new")])
    await message.answer("Выберите проект или создайте новый:", reply_markup=kb(rows))


@router.callback_query(F.data == "proj:new")
async def new_project(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectWizard.name)
    await callback.message.answer("Введите название проекта:")
    await callback.answer()


@router.message(ProjectWizard.name)
async def project_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    if not name or len(name) > 64:
        await message.answer("Название: от 1 до 64 символов.")
        return
    await state.update_data(project_name=name)
    await state.set_state(ProjectWizard.stock)
    await message.answer("Введите размеры заготовки X Y Z в мм. Пример: <code>100 80 20</code>")


@router.message(ProjectWizard.stock)
async def project_stock(message: Message, state: FSMContext):
    try:
        x, y, z = map(float, (message.text or "").replace(",", ".").split())
        if min(x, y, z) <= 0 or x > 1350 or y > 700 or z > 500:
            raise ValueError
        data = await state.get_data()
        pid = create_project(data["project_name"], {"x": x, "y": y, "z": z}, message.from_user.id)
    except (ValueError, TypeError, KeyError):
        await message.answer("Введите X Y Z положительными числами в пределах станка.")
        return
    await state.update_data(active_project_id=pid)
    await state.set_state(None)
    await message.answer(project_summary(get_project(pid, message.from_user.id)), reply_markup=project_kb())


@router.callback_query(F.data.startswith("proj:open:"))
async def open_project(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.rsplit(":", 1)[1])
    project = get_project(pid, callback.from_user.id)
    if project is None:
        await callback.answer("Проект не найден.", show_alert=True)
        return
    await state.clear()
    await state.update_data(active_project_id=pid)
    await callback.message.answer(project_summary(project), reply_markup=project_kb())
    await callback.answer()


@router.callback_query(F.data == "proj:list")
async def project_list(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    projects = list_projects(callback.from_user.id)
    rows = [[(f"📁 {p['name']}", f"proj:open:{p['id']}")] for p in projects[:10]]
    rows.append([("➕ Новый проект", "proj:new")])
    await callback.message.answer("Ваши проекты:", reply_markup=kb(rows))
    await callback.answer()


async def active_project(callback: CallbackQuery, state: FSMContext):
    pid = (await state.get_data()).get("active_project_id")
    return get_project(pid, callback.from_user.id) if pid else None



@router.callback_query(F.data == "proj:preview")
async def preview_project(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project or not project.get("geometry"):
        await callback.answer("Сначала задайте геометрию.", show_alert=True)
        return
    try:
        issues = validate_geometry(project["geometry"])
        if issues:
            await callback.message.answer("Проверка геометрии:\n" + "\n".join("• " + item for item in issues))
        png = render_geometry_preview(project["geometry"])
    except (ValueError, KeyError, TypeError) as exc:
        await callback.answer(str(exc), show_alert=True)
        return
    from aiogram.types import BufferedInputFile
    await callback.message.answer_photo(
        BufferedInputFile(png, filename="geometry_preview.png"),
        caption="Предпросмотр геометрии. Это проверка чертежа, не симуляция обработки.",
    )
    await callback.answer()



@router.callback_query(F.data == "proj:offset")
async def offset_prompt(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project or not project.get("geometry"):
        await callback.answer("Сначала задайте геометрию.", show_alert=True)
        return
    if not project["geometry"].get("closed"):
        await callback.answer("Для смещения нужен замкнутый контур.", show_alert=True)
        return
    await state.set_state(ProjectWizard.offset_tool)
    await callback.message.answer(
        "Введите диаметр фрезы и сторону смещения: <code>D OUTSIDE</code> или <code>D INSIDE</code>.\\n"
        "Пример: <code>10 OUTSIDE</code>. Смещение рассчитывается на радиус фрезы. "
        "Результат будет только предпросмотром, без генерации УП."
    )
    await callback.answer()


@router.message(ProjectWizard.offset_tool)
async def offset_input(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get("active_project_id")
    project = get_project(project_id, message.from_user.id) if project_id else None
    try:
        parts = (message.text or "").replace(",", ".").split()
        if len(parts) != 2:
            raise ValueError("Формат: D OUTSIDE или D INSIDE.")
        diameter = float(parts[0])
        if not math.isfinite(diameter) or diameter <= 0:
            raise ValueError("Диаметр должен быть положительным числом.")
        if parts[1].upper() not in {"OUTSIDE", "INSIDE"}:
            raise ValueError("Сторона: OUTSIDE или INSIDE.")
        if not project or not project.get("geometry"):
            raise ValueError("Проект или геометрия не найдены.")
        shifted = offset_geometry(project["geometry"], diameter / 2, parts[1])
        png = render_geometry_preview(shifted)
    except (ValueError, TypeError, KeyError) as exc:
        await message.answer(f"Смещение не построено: {exc}")
        return
    from aiogram.types import BufferedInputFile
    await state.set_state(None)
    await message.answer_photo(
        BufferedInputFile(png, filename="cutter_offset_preview.png"),
        caption=f"Предпросмотр смещения на R{diameter / 2:g} мм ({parts[1].upper()}). "
                "Это аппроксимация контура, не проверенная траектория и не УП.",
        reply_markup=project_kb(),
    )



@router.callback_query(F.data == "proj:toolpath")
async def toolpath_prompt(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project or not project.get("geometry"):
        await callback.answer("Сначала задайте геометрию.", show_alert=True)
        return
    if not project["geometry"].get("closed"):
        await callback.answer("Нужен замкнутый контур.", show_alert=True)
        return
    await state.set_state(ProjectWizard.profile_diameter)
    await state.update_data(toolpath_values={})
    await callback.message.answer(
        "<b>Шаг 1 из 5. Диаметр фрезы</b>\n"
        "Укажите диаметр режущей части инструмента в миллиметрах. "
        "Например, если фреза Ø10 мм, отправьте <code>10</code>.\n"
        "Введите только число."
    )
    await callback.answer()


@router.message(ProjectWizard.profile_diameter)
async def toolpath_diameter(message: Message, state: FSMContext):
    try:
        value = float((message.text or "").strip().replace(",", "."))
        if not math.isfinite(value) or not 0.1 <= value <= 100:
            raise ValueError
    except ValueError:
        await message.answer("Не понял диаметр. Введите число от 0.1 до 100 мм. Например: <code>10</code>.")
        return
    await state.update_data(toolpath_diameter=value)
    await state.set_state(ProjectWizard.profile_depth)
    await message.answer(
        "<b>Шаг 2 из 5. Глубина обработки</b>\n"
        "На какую глубину нужно обработать контур от верхней поверхности детали? "
        "Введите значение в мм. Например: <code>12</code>."
    )


@router.message(ProjectWizard.profile_depth)
async def toolpath_depth(message: Message, state: FSMContext):
    try:
        value = float((message.text or "").strip().replace(",", "."))
        if not math.isfinite(value) or not 0 < value <= 500:
            raise ValueError
    except ValueError:
        await message.answer("Глубина должна быть больше 0 и не более 500 мм. Например: <code>12</code>.")
        return
    await state.update_data(toolpath_depth=value)
    await state.set_state(ProjectWizard.profile_stepdown)
    await message.answer(
        "<b>Шаг 3 из 5. Глубина одного прохода по Z</b>\n"
        "Это сколько миллиметров фреза опускается за один проход. "
        "Например, при общей глубине 12 мм и шаге 3 мм получится 4 уровня: "
        "3, 6, 9 и 12 мм.\nВведите шаг от 0.01 до 10 мм. Пример: <code>3</code>."
    )


@router.message(ProjectWizard.profile_stepdown)
async def toolpath_stepdown(message: Message, state: FSMContext):
    try:
        value = float((message.text or "").strip().replace(",", "."))
        if not math.isfinite(value) or not 0 < value <= 10:
            raise ValueError
    except ValueError:
        await message.answer("Шаг по Z должен быть больше 0 и не более 10 мм. Например: <code>3</code>.")
        return
    await state.update_data(toolpath_stepdown=value)
    await state.set_state(ProjectWizard.profile_side)
    await message.answer(
        "<b>Шаг 4 из 5. С какой стороны вести фрезу?</b>\n"
        "Выберите вариант:\n"
        "• <b>Снаружи</b> — обработка внешнего контура детали.\n"
        "• <b>Изнутри</b> — обработка внутреннего контура/кармана.",
        reply_markup=kb([[("Снаружи", "proj:toolpath:side:OUTSIDE"),
                          ("Изнутри", "proj:toolpath:side:INSIDE")],
                         [("Отмена", "proj:toolpath:cancel")]])
    )


@router.callback_query(F.data.startswith("proj:toolpath:side:"))
async def toolpath_side(callback: CallbackQuery, state: FSMContext):
    side = callback.data.rsplit(":", 1)[1]
    if side not in {"OUTSIDE", "INSIDE"}:
        await callback.answer("Неизвестный вариант.", show_alert=True)
        return
    await state.update_data(toolpath_side=side)
    await state.set_state(ProjectWizard.profile_allowance)
    await callback.message.answer(
        "<b>Шаг 5 из 5. Припуск на чистовую обработку</b>\n"
        "Припуск — это небольшой слой материала, который оставляют для последующего чистового прохода. "
        "Если чистовой проход пока не планируете, введите <code>0</code>.\n"
        "Допустимо от 0 до 5 мм. Пример: <code>0.2</code>."
    )
    await callback.answer()


@router.callback_query(F.data == "proj:toolpath:cancel")
async def toolpath_cancel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await callback.message.answer("Построение траектории отменено.", reply_markup=project_kb())
    await callback.answer()


@router.message(ProjectWizard.profile_allowance)
async def toolpath_allowance(message: Message, state: FSMContext):
    try:
        allowance = float((message.text or "").strip().replace(",", "."))
        if not math.isfinite(allowance) or not 0 <= allowance <= 5:
            raise ValueError
        data = await state.get_data()
        project_id = data.get("active_project_id")
        project = get_project(project_id, message.from_user.id) if project_id else None
        if not project or not project.get("geometry"):
            raise ValueError("Проект или геометрия не найдены.")
        diameter = data["toolpath_diameter"]
        depth = data["toolpath_depth"]
        stepdown = data["toolpath_stepdown"]
        side = data["toolpath_side"]
        toolpath = build_profile_toolpath(
            project["geometry"], diameter, depth, stepdown, side, allowance
        )
        png = render_toolpath_preview(toolpath)
    except (ValueError, TypeError, KeyError) as exc:
        await message.answer(
            f"Не удалось построить предпросмотр: {exc}\n"
            "Проверьте значение и введите припуск ещё раз (от 0 до 5 мм). "
            "Если чистовой проход не нужен, отправьте <code>0</code>."
        )
        return
    await state.set_state(None)
    await message.answer(
        "<b>Параметры приняты</b>\n"
        f"Фреза: Ø{diameter:g} мм\n"
        f"Глубина: {depth:g} мм\n"
        f"Шаг по Z: {stepdown:g} мм\n"
        f"Сторона: {'снаружи' if side == 'OUTSIDE' else 'изнутри'}\n"
        f"Припуск: {allowance:g} мм\n\n"
        "Строю геометрический предпросмотр..."
    )
    from aiogram.types import BufferedInputFile
    await message.answer_photo(
        BufferedInputFile(png, filename="profile_toolpath_preview.png"),
        caption=(
            f"Предпросмотр: {toolpath['path_count']} проходов, "
            f"{len(toolpath['z_levels'])} уровней Z, длина геометрии "
            f"{toolpath['estimated_cut_length_mm']:.1f} мм.\n"
            "Это только геометрия центра фрезы. Нет врезания, отводов, проверки коллизий и G-кода."
        ),
        reply_markup=project_kb(),
    )


@router.callback_query(F.data == "proj:rounded")
async def rounded_prompt(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project:
        await callback.answer("Сначала откройте проект.", show_alert=True)
        return
    await state.set_state(ProjectWizard.rounded_polygon)
    await callback.message.answer(
        "<b>Контур с разными радиусами углов</b>\n"
        "Введите вершины по порядку, одна на строку: <code>X Y R</code>.\n"
        "R — радиус скругления этой вершины в мм; 0 — острый угол.\n"
        "Пример прямоугольника 80×40 с радиусами 5, 10, 2 и 0:\n"
        "<code>0 0 5\n80 0 10\n80 40 2\n0 40 0</code>\n"
        "Пока поддерживаются выпуклые многоугольники."
    )
    await callback.answer()


@router.message(ProjectWizard.rounded_polygon)
async def rounded_input(message: Message, state: FSMContext):
    data = await state.get_data()
    project_id = data.get("active_project_id")
    try:
        vertices = []
        for line in (message.text or "").splitlines():
            if not line.strip():
                continue
            values = line.replace(",", ".").split()
            if len(values) != 3:
                raise ValueError("Каждая строка должна содержать X Y R.")
            vertices.append(tuple(map(float, values)))
        geometry = build_rounded_polygon(vertices)
        set_geometry(project_id, message.from_user.id, geometry)
    except (ValueError, TypeError) as exc:
        await message.answer(f"Контур не сохранён: {exc}")
        return
    await state.set_state(None)
    await message.answer(
        f"Контур построен и проверен. Сегментов: {len(geometry['segments'])}.",
        reply_markup=project_kb(),
    )


@router.callback_query(F.data == "proj:manual")
async def manual_prompt(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project:
        await callback.answer("Сначала откройте проект.", show_alert=True)
        return
    await state.set_state(ProjectWizard.manual_geometry)
    await callback.message.answer(
        "<b>Построение контура</b>\n"
        "<code>M 0 0</code> — начало; <code>L 50 0</code> — линия;\n"
        "<code>A 50 20 0 10 CCW</code> — дуга (I/J от текущей точки); <code>Z</code> — замкнуть.\n"
        "Одна команда на строку. Координаты в мм."
    )
    await callback.answer()


@router.message(ProjectWizard.manual_geometry)
async def manual_input(message: Message, state: FSMContext):
    pid = (await state.get_data()).get("active_project_id")
    try:
        geometry = parse_manual_path(message.text or "")
        set_geometry(pid, message.from_user.id, geometry)
    except (ValueError, TypeError) as exc:
        await message.answer(f"Ошибка контура: {exc}")
        return
    await state.set_state(None)
    await message.answer(f"Контур сохранён. Сегментов: {len(geometry['segments'])}.", reply_markup=project_kb())


@router.callback_query(F.data == "proj:dxf")
async def dxf_prompt(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project:
        await callback.answer("Сначала откройте проект.", show_alert=True)
        return
    await callback.message.answer("Отправьте DXF-файл документом. Поддерживаются LINE, ARC и полилинии.")
    await callback.answer()


@router.message(F.document)
async def dxf_upload(message: Message, state: FSMContext):
    pid = (await state.get_data()).get("active_project_id")
    doc: Document = message.document
    if not pid or not doc.file_name or not doc.file_name.lower().endswith(".dxf"):
        return
    from io import BytesIO
    stream = BytesIO()
    await message.bot.download(doc, destination=stream)
    try:
        geometry = parse_dxf(stream.getvalue())
        set_geometry(pid, message.from_user.id, geometry)
    except ValueError as exc:
        await message.answer(str(exc))
        return
    await state.set_state(None)
    await message.answer(f"DXF импортирован. Сегментов: {len(geometry['segments'])}. Единицы DXF нужно проверить.", reply_markup=project_kb())


@router.callback_query(F.data.startswith("proj:add:"))
async def add_project_operation(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project:
        await callback.answer("Сначала откройте проект.", show_alert=True)
        return
    kind = callback.data.rsplit(":", 1)[1]
    op_id = add_operation(project["id"], callback.from_user.id, {"type": kind, "status": "draft"})
    await callback.message.answer(f"Операция #{op_id} добавлена как черновик. Настройки обработки подключаются следующим этапом.")
    await callback.answer()


@router.callback_query(F.data == "proj:ops")
async def operations_list(callback: CallbackQuery, state: FSMContext):
    project = await active_project(callback, state)
    if not project:
        await callback.answer("Сначала откройте проект.", show_alert=True)
        return
    body = "\n".join(f"{o['id']}. {o['type']} — {o.get('status', 'draft')}" for o in project["operations"]) or "Операций пока нет."
    await callback.message.answer("<b>Операции проекта</b>\n" + body)
    await callback.answer()
