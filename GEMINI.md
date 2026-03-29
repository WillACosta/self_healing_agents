
# Self-Healing Project Agentic Guidelines

This projects serves as a spec-driven document to describe and list all the decisions and architecture used in this autonomous agents workflow proof of concept.

## Planned Workflow (v1)

We have a fast api in python with some performance issues, and an agentic system that observes the api metrics and logs to try find possible issues in runtime.

If some issue is found, we need to invoke the **performance_agent**  who will receive the metrics and codebase as input to try find where is the error.

Then a **coding_agent** will be invoked to propose a fix or refactor to that specific part of the code to solve the problem.

After that it will generate a `solution.md` with the suggestions.

![agentic_workflow](assets/agentic_workflow.png)

## Key decisions

- We need to implement a way to observe the metrics in the running application, and feed the **performance_agent** with them to look for possible issues. Possible solution: Use cloud functions to schedule analysis.

- The coding agent shouldn't read all the codebase, which would cause an overuse of tokens, due to larger codebases, we need to implement a strategy to look for the most important parts of the code for the given metrics metadata (e.g. logs, stacktraces, etc). Possible solution: send the AST of the codebase to the LLM alongside metrics metadata.
