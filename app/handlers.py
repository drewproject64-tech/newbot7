from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .formatting import format_dt
from .keyboards import back_menu, converter_menu, main_menu, world_clock_menu
from .timezones import city_list, city_now, now_utc, parse_timezone

router = Router()


class ConverterState(StatesGroup):
    waiting_for_input = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, settings):
    await state.clear()
    await message.answer(settings.welcome_message, reply_markup=main_menu())


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "SB24 has three functions:\n\n"
        "🕐 Current Time — current UTC time.\n"
        "🌍 World Clock — current time in selected cities.\n"
        "🔄 Time Zone Converter — convert a date/time between supported time zones.\n\n"
        "Use /start to return to the main menu.",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext, settings):
    await state.clear()
    if callback.message:
        await callback.message.edit_text(settings.welcome_message, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "current_time")
async def current_time(callback: CallbackQuery):
    if callback.message:
        await callback.message.edit_text(
            "🕐 Current Time\n\n"
            + format_dt(now_utc())
            + "\n\nTime shown in UTC.",
            reply_markup=back_menu(),
        )
    await callback.answer()


@router.callback_query(F.data == "world_clock")
async def world_clock(callback: CallbackQuery):
    if callback.message:
        await callback.message.edit_text(
            "🌍 World Clock\n\nSelect a city:",
            reply_markup=world_clock_menu(city_list()),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("city:"))
async def city(callback: CallbackQuery):
    city_key = (callback.data or "").split(":", 1)[1]
    try:
        label, dt = city_now(city_key)
    except ValueError:
        await callback.answer("That city is unavailable.", show_alert=True)
        return

    if callback.message:
        await callback.message.edit_text(
            f"🌍 {label}\n\n{format_dt(dt)}",
            reply_markup=world_clock_menu(city_list()),
        )
    await callback.answer()


@router.callback_query(F.data == "timezone_converter")
async def timezone_converter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ConverterState.waiting_for_input)
    if callback.message:
        await callback.message.edit_text(
            "🔄 Time Zone Converter\n\n"
            "Send one line in this format:\n"
            "YYYY-MM-DD HH:MM | FROM_TIMEZONE | TO_TIMEZONE\n\n"
            "Example:\n"
            "2026-10-01 15:30 | Africa/Lagos | Europe/London",
            reply_markup=converter_menu(),
        )
    await callback.answer()


@router.callback_query(F.data == "converter_sample")
async def converter_sample(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ConverterState.waiting_for_input)
    if callback.message:
        await callback.message.edit_text(
            "🔄 Example input:\n\n"
            "2026-10-01 15:30 | Africa/Lagos | Europe/London\n\n"
            "Send your own value in the same format.",
            reply_markup=back_menu(),
        )
    await callback.answer()


@router.message(ConverterState.waiting_for_input)
async def convert(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    parts = [part.strip() for part in text.split("|")]

    if len(parts) != 3:
        await message.answer(
            "Invalid format. Use:\n"
            "YYYY-MM-DD HH:MM | FROM_TIMEZONE | TO_TIMEZONE\n\n"
            "Example:\n"
            "2026-10-01 15:30 | Africa/Lagos | Europe/London",
            reply_markup=back_menu(),
        )
        return

    try:
        naive = datetime.strptime(parts[0], "%Y-%m-%d %H:%M")
        source_tz = parse_timezone(parts[1])
        target_tz = parse_timezone(parts[2])
        source = naive.replace(tzinfo=source_tz)
        converted = source.astimezone(target_tz)
    except ValueError as exc:
        await message.answer(
            f"Could not convert that value: {exc}",
            reply_markup=back_menu(),
        )
        return

    await state.clear()
    await message.answer(
        "🔄 Time Zone Conversion\n\n"
        f"From: {parts[1]}\n{format_dt(source)}\n\n"
        f"To: {parts[2]}\n{format_dt(converted)}",
        reply_markup=back_menu(),
    )


@router.message()
async def fallback(message: Message):
    await message.answer(
        "Please use one of the three functions below, or send /start.",
        reply_markup=main_menu(),
    )
