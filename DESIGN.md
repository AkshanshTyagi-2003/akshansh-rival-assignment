Design Document — Rival.io API Log Analytics Engine
1. Overview

This document explains the design decisions, architecture, algorithms, trade-offs, and engineering reasoning behind the analytics engine.

The goal was to build a scalable, modular, production-quality system capable of processing thousands of API logs reliably and efficiently.

2. Architectural Breakdown
2.1 Modular File Structure

To ensure maintainability and clean separation of concerns:

function.py
Main orchestrator containing analyze_api_logs()

utils.py
Timestamp parsing, input validation, grouping, frequency analysis

config.py
Threshold values, cost constants, memory pricing brackets

advanced_features.py
Cost estimation engine and caching opportunity analysis

tests/
Full test suite with unit tests, edge cases, performance tests

This mirrors real production backends where business logic is never tightly coupled.

3. Core Logic
3.1 Summary Metrics

Collected in a single O(n) pass:

Response time sum

Error count

Timestamp min/max

Total requests

3.2 Endpoint Statistics

Grouped using a dictionary mapping each endpoint to a list of logs — enabling efficient aggregation without unnecessary nested loops.

3.3 Performance Issue Detection

Thresholds defined in config.py:

medium > 500ms
high > 1000ms
critical > 2000ms


This keeps configuration external and clean.

3.4 Error Rate Detection

Error rates computed per endpoint with severity tiers.

4. Advanced Features
4.1 Cost Estimation Engine (Chosen Feature A)
Why Chosen

Deterministic

Easy to compute

Reflects real cloud billing models

High signal-to-effort ratio

Approach

For each log:

cost = cost_per_request
      + cost_per_ms * response_time_ms
      + memory_cost(response_size_bytes)


Aggregated by endpoint for deeper insights.

4.2 Caching Opportunity Analysis (Chosen Feature D)
Why Chosen

Caching is one of the most impactful backend optimizations.

Criteria

100 requests

80 percent GET

< 2 percent errors

Low response-time variability

These heuristics replicate real load-balancer caching decisions.

5. Edge-Case Handling

Handled in both code and tests:

Empty logs

Malformed logs

Missing fields

Invalid timestamps

Negative numbers

Single log entry

A "fail open but return safe values" strategy was chosen.

6. Performance and Scalability
6.1 Achieved

Processed 10,000 logs in under 2 seconds (test included)

Linear time complexity O(n)

No expensive nested operations

6.2 Scaling to 1M+ Logs

Given more logs:

Use generators / streaming

Convert lists to Pandas DataFrames for vectorization

Use multiprocessing for endpoint-level parallelization

Consider PyPy or Cython if extreme performance is needed

In serverless architecture, shard by time window or endpoint

7. Trade-offs
Simplicity vs. Precision

E.g., caching confidence uses heuristics instead of machine learning.

Modularity vs. Minimal Files

Chose modularity for clarity and extensibility.

Performance vs. Memory

Grouping by endpoint uses additional memory but drastically improves aggregation speed.

8. If Given More Time

I would improve:

Add anomaly detection (request spikes, error clusters)

Add rate-limit violation analysis

Add an interactive HTML report

Add visualization using matplotlib or Plotly

Convert the engine into an installable Python package

9. Time Spent

Approximately 8–9 hours total:

3 hours core logic

2 hours advanced features

1.5 hours testing

45 minutes documentation

30 minutes debugging and polishing