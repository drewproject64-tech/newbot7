import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from .config import load_settings
from .handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("sb24timebot")


async def configure_bot(bot: Bot, settings) -> None:
    await bot.set_my_name(name=settings.bot_name)
    await bot.set_my_short_description(short_description=settings.about_text)
    await bot.set_my_description(description=settings.description)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the main menu"),
            BotCommand(command="help", description="Show how SB24 works"),
        ],
        scope=BotCommandScopeDefault(),
    )


async def main() -> None:
    settings = load_settings()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp["settings"] = settings
    dp.include_router(router)

    try:
        await configure_bot(bot, settings)
        logger.info("SB24 is starting")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
