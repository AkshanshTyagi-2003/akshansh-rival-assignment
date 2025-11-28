Rival.io API Log Analytics Engine

A production-ready serverless analytics engine that processes large API log datasets and generates actionable insights, performance diagnostics, cost estimations, and caching recommendations.

This project is implemented in Python with a strong focus on:

Modular design

Performance

Edge-case safety

Clean code

Comprehensive testing

It fulfills all requirements of the Rival.io internship coding assignment.

🚀 Features
Core Analytics

✔ Total request summary
✔ Time range detection
✔ Average response time
✔ Error-rate calculation
✔ Per-endpoint statistics
✔ Slow endpoint detection
✔ High error-rate detection
✔ Recommendations
✔ Hourly request distribution
✔ Top 5 active users

Advanced Features

✔ Cost Estimation Engine
✔ Caching Opportunity Analysis

Production-Readiness

✔ Input validation
✔ Malformed data handling
✔ Negative value protection
✔ Timestamp parsing
✔ Performance optimized (10k logs < 2 seconds)
✔ Modular structure following best practices

📁 Repository Structure
Akshansh_Rival_Assignment/
├── function.py
├── utils.py
├── config.py
├── advanced_features.py
├── test_run.py
├── tests/
│   ├── test_function.py
│   ├── test_edge_cases.py
│   ├── test_performance.py
│   └── test_data/
│       ├── sample_small.json
│       ├── sample_medium.json
│       └── sample_large.json
├── README.md
└── DESIGN.md

🔧 Setup Instructions
1. Clone the repository
git clone <your_repo_link>
cd Akshansh_Rival_Assignment

2. Install dependencies
python -m pip install -r requirements.txt

3. Run a manual test
python test_run.py

4. Run the full test suite
python -m pytest -v

▶️ Usage Example
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

🧪 Testing Instructions

Run all tests:

python -m pytest -v


The suite covers:

Unit tests

Edge cases

Malformed data

Negative values

Timestamp failures

Performance benchmark

All tests should pass (they do in your current build).

📊 Time and Space Complexity
Time Complexity

O(n) for all log processing

No nested loops dependent on n

Performance tested on 10,000 logs under 2 seconds

Space Complexity

O(n) for grouped data structures

This is optimal for a Python solution.

🧩 Design Summary

See DESIGN.md for detailed architectural decisions.

🧑‍💻 Author

Akshansh Tyagi
Email: akshanshtyagi2003@gmail.com