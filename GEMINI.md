# Self-Healing Project: Agentic Workflow Guidelines

This project serves as a spec-driven document detailing the architecture and decision-making process for an autonomous self-healing agents proof-of-concept (PoC).

## Overview

The system aims to autonomously identify, diagnose, and propose solutions for performance bottlenecks and runtime errors in a Python-based FastAPI application. By leveraging a multi-agent orchestration, the workflow moves from passive observation to proactive refactoring.

## Planned Workflow (v1)

1.  **Observability:** An agentic system continuously monitors the FastAPI application's metrics (e.g., latency, throughput, error rates) and logs.
2.  **Detection & Diagnosis:** Upon detecting an anomaly or performance degradation, the **Performance Agent** is invoked. It analyzes metrics metadata and the codebase to pinpoint the root cause.
3.  **Remediation:** A **Coding Agent** receives the diagnosis and relevant code segments to propose a fix, refactor, or optimization.
4.  **Reporting:** The workflow concludes with the generation of a `solution.md` file, documenting the findings and suggested code changes.

![agentic_workflow](assets/agentic_workflow.png)

## Architecture & Key Decisions

- **Runtime Monitoring:**
  - _Decision:_ The application must expose structured metrics and logs.
  - _Strategy:_ Use OpenTelemetry or Prometheus for instrumentation. A "Monitor Agent" or a scheduled task (e.g., Cloud Function/Cron) will periodically evaluate these metrics against defined SLAs.

- **Context-Aware Analysis (Token Efficiency):**
  - _Decision:_ Avoid passing the entire codebase to the LLM to minimize token consumption and reduce noise.
  - _Strategy:_ Implement a "Code Retrieval" strategy. Use stack traces and log metadata to identify specific modules or functions. Extract the Abstract Syntax Tree (AST) or relevant call graphs for only those components to provide the LLM with surgical context.

- **Validation (Future Iteration):**
  - _Decision:_ Proposing a solution is only half the battle; it must be verified.
  - _Strategy:_ In future versions, a **Validation Agent** should execute unit/integration tests against the proposed fix to ensure correctness and prevent regressions.

## Guidance for Agents

When interacting with this project, agents should:
- Prioritize surgical code reads over full-file reads.
- Use logs and metrics as the primary entry point for debugging.
- Ensure all proposed fixes include a justification based on the provided metrics.

## Project Guidelines

- **Commit Messages:** All commits must follow the [commitlint](https://commitlint.js.org/) format (e.g., `feat: add observability stack`, `fix: correct database seeding logic`).

