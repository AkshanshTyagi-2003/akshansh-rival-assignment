from advanced_features import compute_cost_analysis, compute_caching_opportunities
import datetime
from typing import Any, Dict, List
from collections import Counter

from utils import (
    parse_timestamp,
    validate_log,
    group_by_endpoint,
    group_by_user,
    hourly_buckets,
    most_common
)

from config import (
    RESPONSE_TIME_THRESHOLDS,
    ERROR_RATE_THRESHOLDS
)


def analyze_api_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Main function that processes API logs and returns full analytics.

    Handles:
    - empty arrays
    - malformed logs
    - endpoint statistics
    - performance issue detection
    - error rate detection
    - recommendations
    - hourly distribution
    - top users by request count
    """

    # ---------- Edge case: empty ----------
    if not logs:
        return {
            "summary": {
                "total_requests": 0,
                "time_range": {"start": None, "end": None},
                "avg_response_time_ms": 0,
                "error_rate_percentage": 0
            },
            "endpoint_stats": [],
            "performance_issues": [],
            "recommendations": [],
            "hourly_distribution": {},
            "top_users_by_requests": []
        }

    # ---------- Filter + fix malformed logs ----------
    valid_logs = [log for log in logs if validate_log(log)]

    if not valid_logs:
        return {
            "summary": {
                "total_requests": 0,
                "time_range": {"start": None, "end": None},
                "avg_response_time_ms": 0,
                "error_rate_percentage": 0
            },
            "endpoint_stats": [],
            "performance_issues": [],
            "recommendations": [],
            "hourly_distribution": {},
            "top_users_by_requests": []
        }

    # ----------- Summary calculations -----------
    timestamps = [parse_timestamp(log["timestamp"]) for log in valid_logs]
    timestamps = [t for t in timestamps if t is not None]

    start_time = min(timestamps).isoformat() if timestamps else None
    end_time = max(timestamps).isoformat() if timestamps else None

    total_requests = len(valid_logs)
    avg_resp_time = sum(log["response_time_ms"] for log in valid_logs) / total_requests

    error_count = sum(1 for log in valid_logs if log["status_code"] >= 400)
    error_rate = (error_count / total_requests) * 100

    summary = {
        "total_requests": total_requests,
        "time_range": {"start": start_time, "end": end_time},
        "avg_response_time_ms": round(avg_resp_time, 3),
        "error_rate_percentage": round(error_rate, 3)
    }

    # ------------- Endpoint statistics -------------
    grouped = group_by_endpoint(valid_logs)
    endpoint_stats = []

    for endpoint, logs_ep in grouped.items():

        ep_resp_times = [l["response_time_ms"] for l in logs_ep]
        ep_status_codes = [l["status_code"] for l in logs_ep]

        request_count = len(logs_ep)
        avg_ep_resp = sum(ep_resp_times) / request_count
        slowest = max(ep_resp_times)
        fastest = min(ep_resp_times)

        error_count_ep = sum(1 for l in logs_ep if l["status_code"] >= 400)
        most_common_status = most_common(ep_status_codes)

        endpoint_stats.append({
            "endpoint": endpoint,
            "request_count": request_count,
            "avg_response_time_ms": round(avg_ep_resp, 3),
            "slowest_request_ms": slowest,
            "fastest_request_ms": fastest,
            "error_count": error_count_ep,
            "most_common_status": most_common_status
        })

    # ---------------- Performance Issues -----------------
    performance_issues = []

    for ep in endpoint_stats:
        avg_rt = ep["avg_response_time_ms"]

        if avg_rt > RESPONSE_TIME_THRESHOLDS["critical"]:
            sev = "critical"
        elif avg_rt > RESPONSE_TIME_THRESHOLDS["high"]:
            sev = "high"
        elif avg_rt > RESPONSE_TIME_THRESHOLDS["medium"]:
            sev = "medium"
        else:
            continue

        performance_issues.append({
            "type": "slow_endpoint",
            "endpoint": ep["endpoint"],
            "avg_response_time_ms": avg_rt,
            "threshold_ms": RESPONSE_TIME_THRESHOLDS["medium"],
            "severity": sev
        })

    # ---------------- High Error Rate Issues -----------------
    for ep in endpoint_stats:
        req = ep["request_count"]
        if req == 0:
            continue

        ep_error_rate = (ep["error_count"] / req) * 100

        if ep_error_rate > ERROR_RATE_THRESHOLDS["critical"]:
            sev = "critical"
        elif ep_error_rate > ERROR_RATE_THRESHOLDS["high"]:
            sev = "high"
        elif ep_error_rate > ERROR_RATE_THRESHOLDS["medium"]:
            sev = "medium"
        else:
            continue

        performance_issues.append({
            "type": "high_error_rate",
            "endpoint": ep["endpoint"],
            "error_rate_percentage": round(ep_error_rate, 3),
            "severity": sev
        })

    # ---------------- Recommendations -----------------
    recommendations = []

    for ep in endpoint_stats:
        if ep["request_count"] > 100:
            recommendations.append(
                f"Consider caching for {ep['endpoint']} ({ep['request_count']} requests)."
            )

        if ep["avg_response_time_ms"] > RESPONSE_TIME_THRESHOLDS["medium"]:
            recommendations.append(
                f"Investigate performance of {ep['endpoint']} (avg {ep['avg_response_time_ms']} ms)."
            )

        if ep["error_count"] > 0:
            error_rate_ep = (ep["error_count"] / ep["request_count"]) * 100
            if error_rate_ep > 5:
                recommendations.append(
                    f"Alert: {ep['endpoint']} has {round(error_rate_ep,2)} percent error rate."
                )

    # ---------------- Hourly Distribution ----------------
    hourly = hourly_buckets(valid_logs)

    # ---------------- Top 5 Users ----------------
    user_counts = group_by_user(valid_logs)
    top_users = [
        {"user_id": uid, "request_count": cnt}
        for uid, cnt in Counter(user_counts).most_common(5)
    ]

    # ---------------- Final Output -----------------
    output = {
        "summary": summary,
        "endpoint_stats": endpoint_stats,
        "performance_issues": performance_issues,
        "recommendations": recommendations,
        "hourly_distribution": hourly,
        "top_users_by_requests": top_users
    }

    # ---------- Advanced Features ----------
    adv_cost = compute_cost_analysis(valid_logs, endpoint_stats)
    adv_cache = compute_caching_opportunities(valid_logs, endpoint_stats)

    output.update(adv_cost)
    output.update(adv_cache)

    return output
