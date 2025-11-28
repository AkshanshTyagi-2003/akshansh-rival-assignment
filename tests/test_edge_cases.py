from function import analyze_api_logs


def test_empty_logs():
    result = analyze_api_logs([])
    assert result["summary"]["total_requests"] == 0
    assert result["endpoint_stats"] == []
    assert result["performance_issues"] == []


def test_single_log():
    logs = [{
        "timestamp": "2025-01-15T10:00:00Z",
        "endpoint": "/api/x",
        "method": "GET",
        "response_time_ms": 100,
        "status_code": 200,
        "user_id": "u1",
        "request_size_bytes": 100,
        "response_size_bytes": 200
    }]
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 1
    assert len(result["endpoint_stats"]) == 1


def test_malformed_logs():
    logs = [
        {"timestamp": "invalid", "endpoint": "/api", "method": "GET"}  # missing fields
    ]
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_negative_values():
    logs = [{
        "timestamp": "2025-01-15T10:00:00Z",
        "endpoint": "/api/x",
        "method": "GET",
        "response_time_ms": -10,
        "status_code": 200,
        "user_id": "u1",
        "request_size_bytes": 100,
        "response_size_bytes": 200
    }]
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0
