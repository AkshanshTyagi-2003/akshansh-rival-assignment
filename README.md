# Rival.io API Log Analytics Engine

A production-ready serverless analytics engine that processes large API log datasets and generates actionable insights, performance diagnostics, cost estimations, and caching recommendations.

This project is implemented in Python with a strong focus on:

- Modular design

- Performance

- Edge-case safety

- Clean code

- Comprehensive testing

---

## Features
### Core Analytics

✔ Total request summary<br>
✔ Time range detection<br>
✔ Average response time<br>
✔ Error-rate calculation<br>
✔ Per-endpoint statistics<br>
✔ Slow endpoint detection<br>
✔ High error-rate detection<br>
✔ Recommendations<br>
✔ Hourly request distribution<br>
✔ Top 5 active users<br>

### Advanced Features

✔ Cost Estimation Engine<br>
✔ Caching Opportunity Analysis<br>

### Production-Readiness

✔ Input validation<br>
✔ Malformed data handling<br>
✔ Negative value protection<br>
✔ Timestamp parsing<br>
✔ Performance optimized (10k logs < 2 seconds)<br>
✔ Modular structure following best practices<br>

---

## Repository Structure

```
Akshansh_Rival_Assignment/<br>
├── function.py<br>
├── utils.py<br>
├── config.py<br>
├── advanced_features.py<br>
├── test_run.py<br>
├── tests/<br>
│   ├── test_function.py<br>
│   ├── test_edge_cases.py<br>
│   ├── test_performance.py<br>
│   └── test_data/<br>
│       ├── sample_small.json<br>
│       ├── sample_medium.json<br>
│       └── sample_large.json<br>
├── README.md<br>
└── DESIGN.md<br>
```

---

## Setup Instructions
### 1. Clone the repository
```
git clone <your_repo_link>
cd YourName_Rival_Assignment
```

### 2. Install dependencies
```
python -m pip install -r requirements.txt
```

### 3. Run a manual test
```
python test_run.py
```

### 4. Run the full test suite
```
python -m pytest -v
```

---

## Usage Example
```
from function import analyze_api_logs

logs = [
    {
        "timestamp": "2025-01-15T10:00:00Z",
        "endpoint": "/api/users",
        "method": "GET",
        "response_time_ms": 120,
        "status_code": 200,
        "user_id": "user_001",
        "request_size_bytes": 256,
        "response_size_bytes": 1024
    }
]

print(analyze_api_logs(logs))
```

---

## Testing Instructions

### Run all tests:
```
python -m pytest -v
```


The suite covers:

- Unit tests

- Edge cases

- Malformed data

- Negative values

- Timestamp failures

- Performance benchmark

- All tests should pass (they do in your current build).

---

## Time and Space Complexity
### Time Complexity

- O(n) for all log processing

- No nested loops dependent on n

- Performance tested on 10,000 logs under 2 seconds

Space Complexity

- O(n) for grouped data structures

This is optimal for a Python solution.

## Design Summary

See DESIGN.md for detailed architectural decisions.

---

## Author

Akshansh Tyagi
Email: akshanshtyagi2003@gmail.com

---
