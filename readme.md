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
**Repository:** https://github.com/l3vzNJIT/midterm

---

## 1. Overview

This project is a command-line calculator written in Python that demonstrates modern software engineering principles and professional coding practices. It features a modular plugin architecture based on the Command design pattern, uses environment variables for configuration, and manages a persistent command history via CSV files using the Pandas library. Logging is used throughout for diagnostics, and error handling adheres to the EAFP and LBYL paradigms. The project is structured with testability in mind and supports continuous integration via GitHub Actions.

---

## 2. REPL Command Loop

At the heart of the application is a Read-Eval-Print Loop (REPL), where the user inputs commands that the system interprets and executes. This loop is implemented in `main.py`, which initializes the logging, loads environment configurations, and starts the REPL interface. When a user enters input, it is routed to the `Invoker`, which determines the correct command plugin to handle it. This design allows new commands to be added easily by simply introducing new plugin classes.

📎 [CLI entry point - main.py](https://github.com/l3vzNJIT/midterm/blob/main/calculator/main.py)

---

## 3. Plugin System (Command Pattern)

The calculator supports extensible commands via a plugin system using the Command design pattern. Each plugin implements a shared `Command` interface that defines two essential methods: `scope` and `execute`. The `scope` method is used to determine if a given user input should be handled by this command, and `execute` performs the logic. This pattern ensures a clear separation of concerns and makes it easy to introduce new features.

📎 [Command Interface](https://github.com/l3vzNJIT/midterm/blob/main/calculator/commands/command.py)  
📎 [Plugins Folder](https://github.com/l3vzNJIT/midterm/tree/main/calculator/plugins)

---

## 4. Code Structure and Class Responsibilities

### `Command` Class

This is an abstract base class that defines the contract for all command plugins. It ensures that each plugin implements a `scope` method to determine applicability and an `execute` method to carry out its task. This abstraction allows for consistent plugin behavior and helps maintain a clean and scalable architecture.

### `Invoker` Class

The `Invoker` class is responsible for orchestrating the command execution process. It dynamically loads all available plugins, evaluates which one should handle the input using their `scope` method, and invokes the corresponding `execute` function. It also manages an internal history of command execution for further functionality like logging and persistence.

📎 [Invoker Implementation](https://github.com/l3vzNJIT/midterm/blob/main/calculator/invoker.py)

### `HistoryManager` Class

The `HistoryManager` handles all interactions with the CSV file where the calculation history is stored. It uses the Pandas library to read and write structured data, and enforces the maximum allowed number of stored calculations. It provides methods to load history on startup, save it on shutdown, and manipulate it during runtime.

📎 [HistoryManager](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py)

### `settings.py`

This module handles configuration management by loading environment variables from a `.env` file using the `dotenv` package. These configurations control critical runtime parameters such as file paths and logging levels, allowing the application to be portable and environment-agnostic.

📎 [Settings](https://github.com/l3vzNJIT/midterm/blob/main/calculator/config/settings.py)

### `logger.py`

A centralized logging module sets up a consistent logging configuration that can be reused across the entire application. It supports different logging levels (DEBUG, INFO, ERROR) and logs both to the console and to a file, aiding debugging and professional-grade traceability.

📎 [Logger Setup](https://github.com/l3vzNJIT/midterm/blob/main/calculator/utils/logger.py)

---

## 5. Design Patterns Used

This project makes use of several well-known design patterns:

- **Command Pattern** is used for plugin commands to encapsulate each operation and allow easy extension.
- **Factory Behavior** emerges in the `Invoker`, which instantiates and invokes the appropriate command dynamically.
- **Strategy Pattern** is used as each command encapsulates a distinct behavior for interpreting and executing user input.
- **Facade Pattern** is evident in the `HistoryManager`, which wraps complex file I/O and pandas logic behind a simple interface.
- **Singleton Pattern** is approximated in the `logger`, ensuring consistent configuration across all modules.

---

## 6. History Management with Pandas

The `HistoryManager` module is responsible for persisting and restoring calculation history using CSV files. On startup, the history is loaded into memory using a pandas DataFrame. As new calculations are added, the system ensures that only a fixed number (typically 5) are retained. When the program exits or when specific commands modify history, it is written back to disk. This use of pandas allows for efficient, structured data manipulation and minimizes boilerplate file handling logic.

📎 [CSV History Handling](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py)

---

## 7. Configuration with Environment Variables

All configurable runtime options are managed through a `.env` file, which is read by `settings.py`. This includes:
- Path to the CSV file storing command history.
- Logging verbosity level.
- Limits on number of stored calculations.

Using environment variables follows the 12-factor app methodology, improving portability, separation of config from code, and ease of deployment across environments.

📎 [Environment Settings](https://github.com/l3vzNJIT/midterm/blob/main/calculator/config/settings.py)

---

## 8. Logging

The application uses Python’s built-in `logging` library for structured and configurable logging. Logging is initialized on startup and all internal operations—including command execution, file access, and exceptions—are logged at appropriate levels. This provides valuable insight into the application’s behavior and facilitates debugging without relying on `print()` statements.

📎 [Logging Setup](https://github.com/l3vzNJIT/midterm/blob/main/calculator/utils/logger.py)

---

## 9. Exception Handling (EAFP and LBYL)

This project combines the EAFP (Easier to Ask Forgiveness than Permission) and LBYL (Look Before You Leap) paradigms:
- **EAFP** is used when executing user commands and accessing data that may or may not exist.
- **LBYL** is used when checking for file paths, directory existence, and configuration validity.

This dual approach makes the code both Pythonic and robust.

📎 [LBYL Example](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py#L36)  
📎 [EAFP Example](https://github.com/l3vzNJIT/midterm/blob/main/calculator/main.py#L18)

---

## 10. Testing and CI/CD

Unit tests are written using `pytest` and stored in the `tests/` directory. These cover both command logic and file I/O operations. GitHub Actions is configured to run tests automatically on every push, ensuring continuous integration and safeguarding code quality.

📎 [Test Suite](https://github.com/l3vzNJIT/midterm/tree/main/tests)  
📎 [CI Workflow](https://github.com/l3vzNJIT/midterm/blob/main/.github/workflows/test.yml)

---

## 11. Commit History and Development Flow

The Git commit history reflects structured and incremental development. Each feature or bug fix is implemented in a focused commit, often accompanied by related test changes. This structured approach to version control improves traceability and collaboration readiness.

📎 [Commit History](https://github.com/l3vzNJIT/midterm/commits/main)

---

## 12. Submission Checklist

| Requirement                           | Complete? |
|--------------------------------------|-----------|
| Plugin REPL Architecture              | ✅        |
| CSV + Pandas History Management       | ✅        |
| Environment Variable Usage            | ✅        |
| Logging Implementation                | ✅        |
| LBYL + EAFP Handling                  | ✅        |
| GitHub Actions Integration            | ✅        |
| Minimum 90% Test Coverage             | 🔄        |
| Clean Git Commit History              | ✅        |
| README with Pattern + Logging Explanation | ✅        |

