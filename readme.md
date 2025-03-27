# Lev's Midterm Project
Lev Zelenin - Web Systems Programming - Keith Williams - Spring 2025


## Objective
Implement a simple command line calculator using modern software development methodology.
Modern Python development practice: SOLID, DRY, 12 factor app, design patterns


## Installation and Usage Guide
## Linux
```bash
# Clone the repository
git clone https://github.com/l3vzNJIT/midterm.git
# Go to project folder
cd midterm
# Install required packages - necessary for plugin code to work
pip install -r requirements.txt
# Run (note this command will be available in env through pip install)
run_calculator
# Alternative run
python calculator/main.py
```

# Detailed Documentation with Reference Links


# Midterm Project: Advanced Python Calculator
**Author:** Lev Zelenin  
**Course:** Web Systems Programming – Spring 2025  
**Instructor:** Keith Williams  
**Repo:** [l3vzNJIT/midterm](https://github.com/l3vzNJIT/midterm)

---

## 1. Overview

This project is a command-line calculator application built using modern professional software practices, including:

- A plugin-based REPL architecture using the Command Pattern
- Persistent CSV-based history using Pandas
- Dynamic configuration via environment variables
- Logging system for diagnostics and traceability
- Use of exceptions for error handling (EAFP and LBYL)
- Automated testing and continuous integration with GitHub Actions

---

## 2. Core Functionalities

### REPL Command Loop

- User interacts through a Read-Eval-Print Loop.
- Input is interpreted and routed through dynamically loaded plugin commands.
- The `main.py` file initializes the REPL loop and starts the application.

📎 [CLI entry point](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py)

### Plugin System (Command Pattern)

- Each calculator command (e.g., Add, Subtract, HistoryPrint) is implemented as a plugin.
- Plugins inherit from a shared `Command` interface and are dynamically routed via the `Invoker` class.

📎 [Command Interface](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/command.py)  
📎 [Plugins](https://github.com/l3vzNJIT/midterm/tree/master/calculator/plugins)

---

## 3. Code Structure and Class Responsibilities

### `Command` Interface
Defines the contract for all commands:
- `scope(self, user_input)`: Determines whether the command should handle the input.
- `execute(self, user_input)`: Executes the command’s logic.

### `Invoker`
Routes user input to the appropriate plugin based on the `scope` method.
Maintains command history in memory and in CSV.

📎 [Invoker](https://github.com/l3vzNJIT/midterm/blob/master/calculator/invoker/invoker.py)

### `HistoryManager`
Encapsulates CSV file operations using Pandas. Supports loading and saving calculation history.
Handles serialization and deserialization of calculation objects.

📎 [HistoryManager](https://github.com/l3vzNJIT/midterm/blob/master/calculator/history/history_manager.py)

### `settings.py`
Loads and exposes environment variables (via `dotenv`) for paths, limits, and log configuration.

📎 [Settings](https://github.com/l3vzNJIT/midterm/blob/master/calculator/config/settings.py)

### `logger.py`
Sets up application-wide logging. Ensures that all logs are recorded in a consistent format and location.

📎 [Logger](https://github.com/l3vzNJIT/midterm/blob/master/calculator/utils/logger.py)

---

## 4. Design Patterns Used

| Pattern        | Example                                                                 |
|----------------|-------------------------------------------------------------------------|
| Command        | Encapsulates CLI operations                                             |
| Factory        | `Invoker` dynamically instantiates and routes commands                  |
| Strategy       | Plugins define their own `scope` and `execute` methods                  |
| Facade         | `HistoryManager` abstracts CSV and pandas logic                         |
| Singleton      | `logger` configuration is centralized and reused                        |

---

## 5. History Management with Pandas

- Stores up to 5 recent calculations in a CSV file.
- Automatically loads on startup and saves on exit or history modification.
- Uses Pandas for efficient data reading/writing.

📎 [CSV Logic](https://github.com/l3vzNJIT/midterm/blob/master/calculator/history/history_manager.py)

---

## 6. Configuration with Environment Variables

- CSV path, max history size, and logging config are managed via a `.env` file.
- Avoids hardcoded paths and allows flexible deployment.

📎 [Env Settings](https://github.com/l3vzNJIT/midterm/blob/master/calculator/config/settings.py)

---

## 7. Logging

- Uses Python’s built-in `logging` module.
- Logs errors, file I/O, command executions, and more.
- Can switch verbosity via `.env` config.

📎 [Logging Config](https://github.com/l3vzNJIT/midterm/blob/master/calculator/utils/logger.py)

---

## 8. Exception Handling

- EAFP style used when reading files or routing user input.
- LBYL used when verifying file paths or directory existence.

📎 [LBYL Example](https://github.com/l3vzNJIT/midterm/blob/master/calculator/history/history_manager.py#L36)  
📎 [EAFP Example](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py#L18)

---

## 9. Testing and CI/CD

- Tests written using `pytest`.
- GitHub Actions run tests automatically.
- Goal is 90%+ code coverage.

📎 [Tests](https://github.com/l3vzNJIT/midterm/tree/master/tests)  
📎 [GitHub Actions Workflow](https://github.com/l3vzNJIT/midterm/blob/master/.github/workflows/test.yml)

---

## 11. Commit History

Commits reflect:
- Incremental feature development
- Bug fixes and refactoring
- Integrated test creation

📎 [Commit History](https://github.com/l3vzNJIT/midterm/commits/master)

---

## 12. Submission Checklist

| Requirement                           | Complete? |
|--------------------------------------|-----------|
| Plugin REPL Architecture              | ✅        |
| CSV + Pandas History Management       | ✅        |
| Environment Variable Usage            | ✅        |
| Logging Implementation                | ✅        |
| LBYL + EAFP Handling                  | ✅        |
| 3–5 Min Demo Video                    | 🔲        |
| GitHub Actions Integration            | ✅        |
| Minimum 90% Test Coverage             | 🔄        |
| Clean Git Commit History              | ✅        |
| README with Pattern + Logging Explanation | ✅        |
