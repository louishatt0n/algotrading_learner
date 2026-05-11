# Python Basics (Intermediate Bridge)

## Key Terms

- **Module**: A Python file that can be imported.
- **Function**: Reusable code block defined with `def`.
- **Scope**: Where variables are visible and usable.
- **Exception**: Runtime error that interrupts normal flow.

## Core Explanation

To understand this project, you must be comfortable with:

1. Variables and types (`float`, `int`, `str`, `list`, `dict`, `DataFrame`).
2. Functions with parameters and return values.
3. Imports and module namespaces (`module.function()`).
4. Control flow (`if`, `for`, `continue`, `break`).
5. Basic debugging from traceback messages.

## Worked Example

```python
def annualize_return(total_return, days):
    if days <= 0:
        return 0.0
    return (1 + total_return) ** (252 / days) - 1
```

This pattern appears throughout backtests: validate inputs, then compute metric safely.

## Command Reference Or Code Patterns

```python
try:
    value = 1 / x
except ZeroDivisionError:
    value = 0
```

```python
import numpy as np
arr = np.array([1, 2, 3])
```

## Advanced

### Deeper Concepts
- Strong Python practice combines syntax fluency with problem decomposition: break large tasks into testable functions.
- Learn core data structures deeply (lists, dicts, sets, tuples) and choose structures based on operation complexity and semantics.
- Use exceptions and input validation as deliberate program design tools, not afterthoughts.
- Develop a progression from scripts to reusable modules with clear function signatures and docstrings.

### Free Platforms and Courses
- [Python documentation](https://docs.python.org/3/) for authoritative language and standard-library reference.
- [Python getting started tutorials](https://www.python.org/about/gettingstarted/) for guided beginner-to-intermediate progression.
- [CS50 Python](https://cs50.harvard.edu/python) for free structured coursework and exercises.
- [MIT OpenCourseWare](https://ocw.mit.edu/) for complementary computing courses that strengthen algorithmic thinking.

### Practice Path
- Complete one focused Python concept each day (control flow, functions, files, modules, exceptions) with a short script artifact.
- Refactor earlier scripts into reusable functions and compare readability and testability.
- Write small docstrings and input assumptions for every non-trivial function.
- Create a personal error log: record bugs, root causes, and prevention patterns.

### Suggested Mini-Projects
- Build a command-line utility that ingests a file, validates input, and outputs structured results.
- Create a mini test suite for your utility using straightforward assertion-based checks.
- Implement a small data pipeline from raw input to cleaned summary output to prepare for pandas work.
