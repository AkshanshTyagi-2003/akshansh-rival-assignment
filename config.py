# Configuration values and constants for the Rival.io assignment

RESPONSE_TIME_THRESHOLDS = {
    "medium": 500,
    "high": 1000,
    "critical": 2000
}

ERROR_RATE_THRESHOLDS = {
    "medium": 5,
    "high": 10,
    "critical": 15
}

COST_PER_REQUEST = 0.0001
COST_PER_MS = 0.000002

MEMORY_COST_BRACKETS = [
    (0, 1024, 0.00001),
    (1024, 10240, 0.00005),
    (10240, float("inf"), 0.0001)
]
