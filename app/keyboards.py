from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕐 Current Time", callback_data="current_time")],
        [InlineKeyboardButton(text="🌍 World Clock", callback_data="world_clock")],
        [InlineKeyboardButton(text="🔄 Time Zone Converter", callback_data="timezone_converter")],
    ])

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Main Menu", callback_data="main_menu")]
    ])

def world_clock_menu(cities: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=label, callback_data=f"city:{key}")] for label, key in cities]
    rows.append([InlineKeyboardButton(text="← Main Menu", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def converter_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Use a sample", callback_data="converter_sample")],
        [InlineKeyboardButton(text="← Main Menu", callback_data="main_menu")],
    ])
