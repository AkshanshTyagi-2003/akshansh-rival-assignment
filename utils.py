import datetime
from typing import Any, Dict, List, Tuple


def parse_timestamp(ts: str):
    """Convert ISO timestamp to datetime object. Returns None if invalid."""
    try:
        return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def validate_log(entry: Dict[str, Any]) -> bool:
    """Validate presence of required fields and correct value types."""
    required = [
        "timestamp", "endpoint", "method", "response_time_ms",
        "status_code", "user_id", "request_size_bytes", "response_size_bytes"
    ]

    for key in required:
        if key not in entry:
            return False

    if entry["response_time_ms"] < 0:
        return False
    if entry["request_size_bytes"] < 0:
        return False
    if entry["response_size_bytes"] < 0:
        return False

    return True


def group_by_endpoint(logs: List[Dict]) -> Dict[str, List[Dict]]:
    """Group logs by endpoint."""
    grouped = {}
    for log in logs:
        ep = log["endpoint"]
        grouped.setdefault(ep, []).append(log)
    return grouped


def group_by_user(logs: List[Dict]) -> Dict[str, int]:
    """Count number of requests per user."""
    users = {}
    for log in logs:
        uid = log["user_id"]
        users[uid] = users.get(uid, 0) + 1
    return users


def hourly_buckets(logs: List[Dict]) -> Dict[str, int]:
    """Return distribution of requests per hour."""
    buckets = {}
    for log in logs:
        ts = parse_timestamp(log["timestamp"])
        if not ts:
            continue
        hour_key = ts.strftime("%H:00")
        buckets[hour_key] = buckets.get(hour_key, 0) + 1
    return buckets


def most_common(lst: List[Any]) -> Any:
    """Return most common element in a list."""
    if not lst:
        return None
    return max(set(lst), key=lst.count)
