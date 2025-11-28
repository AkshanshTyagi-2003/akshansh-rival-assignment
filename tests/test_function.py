import json
import os
from function import analyze_api_logs


def load_sample(name: str):
    """Load JSON from tests/test_data folder."""
    base = os.path.dirname(__file__)
    path = os.path.join(base, "test_data", name)
    with open(path, "r") as f:
        return json.load(f)


def test_summary_basic():
    logs = load_sample("sample_small.json")
    result = analyze_api_logs(logs)

    assert "summary" in result
    assert result["summary"]["total_requests"] == len(logs)
    assert result["summary"]["avg_response_time_ms"] >= 0


def test_endpoint_stats_structure():
    logs = load_sample("sample_small.json")
    result = analyze_api_logs(logs)

    stats = result["endpoint_stats"]
    assert isinstance(stats, list)
    assert "endpoint" in stats[0]
    assert "request_count" in stats[0]


def test_performance_issues_present():
    logs = load_sample("sample_small.json")
    result = analyze_api_logs(logs)

    assert "performance_issues" in result
    assert isinstance(result["performance_issues"], list)


def test_advanced_cost_analysis_exists():
    logs = load_sample("sample_small.json")
    result = analyze_api_logs(logs)

    assert "cost_analysis" in result
    assert "total_cost_usd" in result["cost_analysis"]


def test_caching_opportunities_exists():
    logs = load_sample("sample_small.json")
    result = analyze_api_logs(logs)

    assert "caching_opportunities" in result
    assert "total_potential_savings" in result
