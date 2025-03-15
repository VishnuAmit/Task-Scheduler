# Concurrent Task Scheduler with Dependency Management

A Python-based task scheduler that manages and executes tasks based on their dependencies while respecting constraints such as maximum concurrency, timeouts, and failure handling.

## Overview
This project implements a **Task Scheduler** that ensures tasks execute in the correct order and tracks their execution results. It's designed to handle complex task dependencies while maintaining configurable execution parameters.

## Features

- **✅ Dependency Management**: Ensures tasks are executed in the correct order.
- **⚡ Concurrency Control**: Supports a configurable number of concurrent task executions.
- **⏳ Timeout Management**: Stops execution when the overall timeout is reached.
- **🛑 Start Threshold Timeout**: Prevents new tasks from starting after a set percentage of the total timeout.
- **🔄 Failure Handling**: Retries failed tasks up to 2 times before marking them as failed.
- **📜 Logging**: Records task execution details, including start time, end time, and duration.
- **🧪 Unit Testing**: Comprehensive tests written using PyTest.

## Installation

Ensure you have **Python 3.8+** installed on your system.

Clone the repository:

```bash
git clone https://github.com/yourusername/task-scheduler.git
cd task-scheduler
```

## Usage

Run the Task Scheduler with a sample input:

```bash
python task_scheduler.py
```

## Input Format

The scheduler expects the following inputs:

- `tasks`: List of unique task identifiers.
- `dependencies`: List of tuples representing task dependencies (A, B), meaning B depends on A.
- `max_workers`: Maximum number of concurrent task executions.
- `timeout`: Total execution time in seconds.
- `start_threshold_timeout`: Percentage of the total timeout after which new tasks cannot be started.

## Example Input

```python
tasks = ["A", "B", "C", "D"]
dependencies = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
timeout = 30
start_threshold_timeout = 0.8
```

## Output Format

The scheduler returns a dictionary with task execution results:

```json
{
  "successful": ["A", "B"],
  "failed": ["C"],
  "canceled": ["D"],
  "unfinished": []
}
```

## Unit Testing

Tests are implemented using PyTest.  
Run the tests with:

```bash
python -m pytest unit_test.py
```

## Contribution

Sometimes, it malfunctions with concurrency turned on. If you can fix that, kindly create an issue and raise a PR. I would be happy to see that getting fixed. 🎯
