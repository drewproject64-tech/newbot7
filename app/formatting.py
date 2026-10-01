from datetime import datetime

def format_dt(dt: datetime, include_zone_name: bool = True) -> str:
    zone_name = getattr(dt.tzinfo, "key", None) if dt.tzinfo else None
    suffix = f" ({zone_name})" if include_zone_name and zone_name else ""
    return dt.strftime("%A, %d %B %Y\n%H:%M:%S") + suffix
