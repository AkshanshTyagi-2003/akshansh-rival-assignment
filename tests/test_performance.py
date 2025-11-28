import time
from function import analyze_api_logs


def test_performance_10000_logs():
    logs = []

    for i in range(10000):
        logs.append({
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": f"user_{i % 10}",
            "request_size_bytes": 300,
            "response_size_bytes": 1500
        })

    start = time.time()
    analyze_api_logs(logs)
    end = time.time()

    assert (end - start) < 2.0
