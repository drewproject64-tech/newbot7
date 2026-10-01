from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CITY_TIMEZONES: dict[str, tuple[str, str]] = {
    "lagos": ("🇳🇬 Lagos", "Africa/Lagos"),
    "london": ("🇬🇧 London", "Europe/London"),
    "new_york": ("🇺🇸 New York", "America/New_York"),
    "los_angeles": ("🇺🇸 Los Angeles", "America/Los_Angeles"),
    "chicago": ("🇺🇸 Chicago", "America/Chicago"),
    "toronto": ("🇨🇦 Toronto", "America/Toronto"),
    "sao_paulo": ("🇧🇷 São Paulo", "America/Sao_Paulo"),
    "dubai": ("🇦🇪 Dubai", "Asia/Dubai"),
    "mumbai": ("🇮🇳 Mumbai", "Asia/Kolkata"),
    "singapore": ("🇸🇬 Singapore", "Asia/Singapore"),
    "tokyo": ("🇯🇵 Tokyo", "Asia/Tokyo"),
    "sydney": ("🇦🇺 Sydney", "Australia/Sydney"),
}

def now_utc() -> datetime:
    return datetime.now(ZoneInfo("UTC"))

def city_list() -> list[tuple[str, str]]:
    return [(label, key) for key, (label, _) in CITY_TIMEZONES.items()]

def city_now(city_key: str) -> tuple[str, datetime]:
    if city_key not in CITY_TIMEZONES:
        raise ValueError("Unknown city.")
    label, tz_name = CITY_TIMEZONES[city_key]
    return label, datetime.now(ZoneInfo(tz_name))

def parse_timezone(tz_name: str) -> ZoneInfo:
    value = tz_name.strip()
    if not value or len(value) > 64:
        raise ValueError("Invalid time zone.")
    try:
        return ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        raise ValueError("Unknown IANA time zone.") from exc
