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

This project is a command-line calculator written in Python that demonstrates modern software engineering principles and professional coding practices. It features a modular plugin architecture based on the Command design pattern, uses environment variables for configuration, and manages a persistent command history via CSV files using the Pandas library. Logging is used throughout for diagnostics, and error handling adheres to the EAFP and LBYL paradigms. The project is structured with testability in mind and includes GitHub Actions for CI/CD.

---

## 2. REPL Command Loop

At the heart of the application is a Read-Eval-Print Loop (REPL), where the user inputs commands that the system interprets and executes. This loop is implemented in `main.py`, which initializes the logging, loads environment configurations, and starts the REPL interface. When a user enters input, it is routed to the `Invoker`, which determines the correct command plugin to handle it.

📎 [CLI entry point - main.py](https://github.com/l3vzNJIT/midterm/blob/main/calculator/main.py)

---

## 3. Plugin System (Command Pattern)

The calculator supports extensible commands via a plugin system using the Command design pattern. Each plugin implements a shared `Command` interface that defines two essential methods: `scope` and `execute`. The `scope` method is used to determine if a given user input should be handled by this command, and `execute` performs the logic. This pattern ensures a clear separation of concerns and makes it easy to introduce new features.

📎 [Command Interface](https://github.com/l3vzNJIT/midterm/blob/main/calculator/commands/command.py)  
📎 [Plugins Folder](https://github.com/l3vzNJIT/midterm/tree/main/calculator/plugins)

---

## 4. Code Structure and Class Responsibilities

### `Command` Class

This abstract base class defines the contract for all command plugins. It ensures that each plugin implements a `scope` method to determine applicability and an `execute` method to carry out its task.

### `Invoker` Class

The `Invoker` orchestrates command execution. It loads all available plugins, checks which one should respond to input, and delegates execution accordingly. It also handles the command history.

📎 [Invoker Implementation](https://github.com/l3vzNJIT/midterm/blob/main/calculator/invoker.py)

### `HistoryManager` Class

Handles persistence of command history using CSV files and Pandas. It reads history into memory on startup, enforces a 5-entry limit, and saves the history when changes occur.

📎 [HistoryManager](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py)

### `settings.py`

Loads runtime configuration from a `.env` file using the `dotenv` package. This includes CSV path, logging level, and other adjustable parameters.

📎 [Settings](https://github.com/l3vzNJIT/midterm/blob/main/calculator/config/settings.py)

### `logger.py`

Central logging configuration used across the app. Initializes handlers and formats to ensure logs are clean, searchable, and consistently stored.

📎 [Logger Setup](https://github.com/l3vzNJIT/midterm/blob/main/calculator/utils/logger.py)

---

## 5. Design Patterns Used

- **Command Pattern**: Encapsulates calculator commands.
- **Factory Behavior**: `Invoker` routes and instantiates commands.
- **Strategy Pattern**: Each plugin defines how it handles input and execution.
- **Facade Pattern**: `HistoryManager` simplifies CSV/pandas operations.
- **Singleton**: Centralized logging configuration.

---

## 6. History Management with Pandas

`HistoryManager` reads and writes structured data to a CSV using Pandas. On startup, it loads previous calculations. If the max size (5) is exceeded, it raises an exception. This ensures performance and manageable memory use.

📎 [CSV History Handling](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py)

---

## 7. Configuration with Environment Variables

`.env` configures file paths, logging level, and history limits. This adheres to the 12-factor app model by externalizing configuration.

📎 [Environment Settings](https://github.com/l3vzNJIT/midterm/blob/main/calculator/config/settings.py)

---

## 8. Logging

Every part of the application uses structured logging. Instead of `print()`, it logs debug, info, and error messages. This approach supports better diagnostics and CI analysis.

📎 [Logging Setup](https://github.com/l3vzNJIT/midterm/blob/main/calculator/utils/logger.py)

---

## 9. Exception Handling (EAFP and LBYL)

- **EAFP**: Try executing risky operations, and handle errors if they occur.
- **LBYL**: Check for file paths or directory existence beforehand.

📎 [LBYL Example](https://github.com/l3vzNJIT/midterm/blob/main/calculator/history/history_manager.py#L36)  
📎 [EAFP Example](https://github.com/l3vzNJIT/midterm/blob/main/calculator/main.py#L18)

---

## 10. Testing and CI/CD

The `tests/` directory includes unit tests that verify functionality across plugins and file handling. GitHub Actions is set up to automatically run tests on push.

📎 [Test Suite](https://github.com/l3vzNJIT/midterm/tree/main/tests)  
📎 [GitHub Actions Workflow](https://github.com/l3vzNJIT/midterm/blob/main/.github/workflows/test.yml)

---

## 11. Commit History and Development Flow

Commits follow a structured flow: each change adds a logical piece of functionality, typically including relevant tests and doc updates. This enables traceable, auditable history.

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
