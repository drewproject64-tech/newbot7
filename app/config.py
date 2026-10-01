import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_name: str = "SB24"
    bot_username: str = "@SB24TimeBot"
    about_text: str = "SB24 shows current time, world clocks, and time zone conversions directly in Telegram."
    description: str = (
        "SB24 is a focused time utility. Check the current time, view clocks for "
        "different cities, and convert times between supported time zones directly in Telegram."
    )
    welcome_message: str = (
        "Welcome to SB24.\n\n"
        "Use the three buttons below to check the current time, view a world clock, "
        "or convert a time between time zones."
    )

def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required.")
    return Settings(bot_token=token)
