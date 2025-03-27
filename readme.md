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

# Midterm Project: Advanced Python Calculator
**Author:** Lev Zelenin  
**Course:** Web Systems Programming – Spring 2025  
**Instructor:** Keith Williams  
**Repository:** https://github.com/l3vzNJIT/midterm

---

## 1. Overview

This project implements a command-line calculator in Python, with a focus on professional software development methodologies. It features a plugin-based architecture utilizing the Command pattern, persistent history management with CSV, structured logging, and testable modular design. Configuration is environment-based, following 12-factor app principles, and the system supports CI/CD integration with GitHub Actions.

---

## 2. REPL Command Loop

The REPL loop is managed through [`main.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py), which initializes logging, loads environment configurations, and loops for user input. Input is passed to the `Invoker` class to determine which plugin should handle the command.

---

## 3. Plugin System and Command Pattern

The `Command` interface is defined in [`command.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/command.py). Each plugin class implements `scope(input: str)` to determine applicability and `execute(input: str)` to perform actions. This structure promotes modular design and ease of extensibility.

Plugins are stored in the [`plugins/`](https://github.com/l3vzNJIT/midterm/tree/master/calculator/plugins) directory. Examples include arithmetic operations (`add`, `subtract`, etc.) and history operations (`HistoryAdd`, `HistoryPrint`, etc.).

---

## 4. Class Responsibilities

### `Invoker`
Located in [`invoker.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/invoker.py), this class is responsible for scanning available plugins, routing input to the correct command based on `scope()`, and invoking execution. It also stores the runtime history of commands executed during the session.

### `HistoryManager`
Implemented within [`history.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/history.py), it handles reading and writing the persistent history to a CSV file using `pandas`. It ensures no more than five history records are stored and provides methods for addition, deletion, and reloading.

### `Logger`
Logging is set up through [`logger.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/logger.py), configuring file and console output. Logging replaces print debugging and is used for all diagnostics.

---

## 5. Environment Configuration

This project follows the 12-factor methodology by storing file paths and settings in environment variables. These are loaded via `dotenv` in the REPL entry file. The history CSV location, logging level, and history record limit are all configured externally.

---

## 6. Design Patterns in Use

- **Command Pattern:** Each plugin command encapsulates user input processing.
- **Factory-Like Behavior:** `Invoker` selects and dispatches commands at runtime.
- **Strategy:** Plugins define their own logic for input matching and execution.
- **Logging Abstraction:** Centralized logger handles application-wide diagnostics.

---

## 7. Exception Handling

- **EAFP (Easier to Ask Forgiveness than Permission):** Used for loading files and runtime operations that might fail.
- **LBYL (Look Before You Leap):** Used for validating directory existence and configurations before use.

Examples:
- [`main.py` usage](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py#L18)
- [`history.py` LBYL logic](https://github.com/l3vzNJIT/midterm/blob/master/calculator/history.py#L36)

---

## 8. Testing and CI/CD

Tests are located in the [`tests/`](https://github.com/l3vzNJIT/midterm/tree/master/tests) directory and include unit coverage for each plugin and utility. GitHub Actions runs tests via [`test.yml`](https://github.com/l3vzNJIT/midterm/blob/master/.github/workflows/test.yml) to ensure build integrity.

---

## 9. Commit History and Practices

Commits in the [master branch](https://github.com/l3vzNJIT/midterm/commits/master) reflect incremental development, feature-based commits, and associated test additions. The structure follows good commit hygiene for clarity and traceability.

---

## 10. Submission Checklist

| Requirement                                | Complete? |
|-------------------------------------------|-----------|
| Plugin-based REPL                         | ✅        |
| CSV + Pandas History Management           | ✅        |
| Environment Variable Usage                | ✅        |
| Logging via `logger.py`                   | ✅        |
| EAFP + LBYL Handling                      | ✅        |
| CI via GitHub Actions                     | ✅        |
| 90%+ Test Coverage                        | 🔄        |
| Clean Commit History                      | ✅        |
| README and Technical Explanation          | ✅        |

