from typing import Dict, List, Any
from config import COST_PER_REQUEST, COST_PER_MS, MEMORY_COST_BRACKETS


# -------------------------------------------------------
# COST ANALYSIS ENGINE (Advanced Feature A)
# -------------------------------------------------------

def get_memory_cost(size_bytes: int) -> float:
    """Return memory cost based on response_size_bytes."""
    for lower, upper, cost in MEMORY_COST_BRACKETS:
        if lower <= size_bytes < upper:
            return cost
    return 0.0


def compute_cost_analysis(logs: List[Dict[str, Any]], endpoint_stats: List[Dict]) -> Dict[str, Any]:
    """Compute total cost and cost per endpoint."""
    
    total_request_cost = 0
    total_execution_cost = 0
    total_memory_cost = 0

    cost_by_endpoint = {}

    for log in logs:
        ep = log["endpoint"]

        # cost per request
        req_cost = COST_PER_REQUEST

        # cost per millisecond of execution
        exec_cost = log["response_time_ms"] * COST_PER_MS

        # memory bracket cost
        mem_cost = get_memory_cost(log["response_size_bytes"])

        total_cost = req_cost + exec_cost + mem_cost

        # aggregate totals
        total_request_cost += req_cost
        total_execution_cost += exec_cost
        total_memory_cost += mem_cost

        # per-endpoint aggregation
        if ep not in cost_by_endpoint:
            cost_by_endpoint[ep] = 0
        cost_by_endpoint[ep] += total_cost

    # convert to required output structure
    endpoint_cost_struct = [
        {
            "endpoint": ep,
            "total_cost": round(total, 6),
            "cost_per_request": round(total / next(e["request_count"] for e in endpoint_stats if e["endpoint"] == ep), 6)
        }
        for ep, total in cost_by_endpoint.items()
    ]

    total_cost = total_request_cost + total_execution_cost + total_memory_cost

    return {
        "cost_analysis": {
            "total_cost_usd": round(total_cost, 6),
            "cost_breakdown": {
                "request_costs": round(total_request_cost, 6),
                "execution_costs": round(total_execution_cost, 6),
                "memory_costs": round(total_memory_cost, 6),
            },
            "cost_by_endpoint": endpoint_cost_struct,
            "optimization_potential_usd": round(total_execution_cost * 0.3, 6)  # example assumption
        }
    }



# -------------------------------------------------------
# CACHING OPPORTUNITY ANALYSIS (Advanced Feature D)
# -------------------------------------------------------

def compute_caching_opportunities(logs: List[Dict[str, Any]], endpoint_stats: List[Dict]) -> Dict[str, Any]:
    """
    Identify endpoints that benefit from caching:
    - More than 100 requests
    - GET requests > 80%
    - Error rate < 2%
    - Consistent response time (std deviation rule, simplified)
    """

    from statistics import stdev

    caching = []
    total_saved_requests = 0
    total_cost_savings = 0
    total_perf_improvement = 0

    endpoints = {}

    # collect logs per endpoint
    for log in logs:
        ep = log["endpoint"]
        if ep not in endpoints:
            endpoints[ep] = []
        endpoints[ep].append(log)

    for ep, ep_logs in endpoints.items():
        if len(ep_logs) < 5:
            continue

        total_requests = len(ep_logs)
        get_count = sum(1 for l in ep_logs if l["method"] == "GET")
        error_count = sum(1 for l in ep_logs if l["status_code"] >= 400)
        resp_times = [l["response_time_ms"] for l in ep_logs]

        get_ratio = (get_count / total_requests) * 100
        error_rate = (error_count / total_requests) * 100

        # rule checks
        if total_requests <= 100:
            continue
        if get_ratio < 80:
            continue
        if error_rate > 2:
            continue

        # response consistency check
        try:
            variability = stdev(resp_times)
        except:
            variability = 0

        if variability > 300:  # too variable
            continue

        potential_hit_rate = round(get_ratio, 2)
        potential_saved = int(total_requests * (get_ratio / 100))

        saved_cost = potential_saved * (0.0001 + 150 * 0.000002)
        perf_improvement = potential_saved * 80  # approximate saved ms

        caching.append({
            "endpoint": ep,
            "potential_cache_hit_rate": potential_hit_rate,
            "current_requests": total_requests,
            "potential_requests_saved": potential_saved,
            "estimated_cost_savings_usd": round(saved_cost, 6),
            "recommended_ttl_minutes": 15,
            "recommendation_confidence": "high"
        })

        total_saved_requests += potential_saved
        total_cost_savings += saved_cost
        total_perf_improvement += perf_improvement

    return {
        "caching_opportunities": caching,
        "total_potential_savings": {
            "requests_eliminated": total_saved_requests,
            "cost_savings_usd": round(total_cost_savings, 6),
            "performance_improvement_ms": total_perf_improvement
        }
    }
