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


# Detailed paper with cited examples in the code

---

## 1. Overview

This project implements a command-line calculator in Python, with a focus on professional software development methodologies. It features a plugin-based architecture utilizing the Command pattern, persistent history management with CSV using pandas, structured logging via the built-in `logging` module, and a modular design conducive to testing and maintenance. Configuration is managed using environment variables, following 12-factor app principles. The project also integrates CI/CD through GitHub Actions.

---

## 2. REPL Command Loop

The REPL loop is initiated by [`main.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py). This script handles environment setup, initializes logging based on the `logging.conf` file, and starts the main input loop. User inputs are passed to the `Invoker` class to determine the appropriate plugin for execution.

---

## 3. Plugin System and Command Pattern

The `Command` interface defined in [`command.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/command.py) serves as the contract for all commands. Each plugin must implement the `scope()` method to determine if it can handle the input, and `execute()` to perform the operation.

Supported plugins include:
- [`add.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/add/add.py): Adds two or more numbers.
- [`subtract.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/subtract/subtract.py): Subtracts one number from another.
- [`multiply.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/multiply/multiply.py): Multiplies numbers.
- [`divide.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/divide/divide.py): Divides numbers with error handling for division by zero.

History-related plugins include:
- [`history_print.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history_print.py): Outputs saved command history from the CSV.
- [`history_clear.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history_clear.py): Clears the entire history file.
- [`history_delete.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history_delete.py): Deletes a specific record by index.
- [`history.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history.py): Shared logic for reading and writing to the history CSV file.

---

## 4. Class Responsibilities

### `Invoker`
Defined in [`invoker.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/invoker.py), this class scans the command directory at runtime and loads available command classes. It calls `scope()` on each to determine the right command for a given input. This modular approach enables extensibility without modifying the REPL core.

### Command Input/Output
- [`command_input.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/command_input.py) provides utilities to normalize and validate input before routing to commands.
- [`command_output.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/command_output.py) standardizes output formatting for consistency.

### History Handling
- [`history.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history.py) acts as the central history module, providing methods for loading from and saving to the CSV history file. It uses `pandas` for fast file-based data operations.
- Other history plugins (`clear`, `delete`, `print`) call this module to read or manipulate the stored command history.

### Logging
Logging is initialized in `main.py` and configured using [`logging.conf`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/logging.conf). Logs are written to a file and provide insight into each major application event. This includes successful command execution, errors, and exceptions.

---

## 5. Environment Configuration

Runtime environment setup is handled by:
- [`setup_env.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/setup_env.py): Loads environment variables and prepares paths for logging and history persistence.
- `.env`: A file (excluded from version control) specifying paths, limits, and logging levels.
- The system uses `python-dotenv` to read these variables at startup.

This enables flexible configuration across environments and supports practices like using relative/absolute paths and injecting test-specific variables.

---

## 6. Design Patterns in Use

- **Command Pattern**: Each plugin follows a consistent interface, simplifying dispatch.
- **Factory Pattern**: The `Invoker` behaves like a factory for selecting and executing commands.
- **Strategy Pattern**: Different plugins implement their own logic while conforming to a shared interface.
- **Separation of Concerns**: Configuration, logging, input/output, and plugin logic are modular.

---

## 7. Exception Handling

The code adheres to both:
- **EAFP (Easier to Ask Forgiveness than Permission)**: Most plugin operations attempt actions (like file reads) and catch exceptions.
- **LBYL (Look Before You Leap)**: Used in `setup_env.py` and `history.py` to ensure paths exist and files are readable.

Examples:
- [`main.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py#L18): Handles REPL and top-level exceptions.
- [`history.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history.py): Manages file access safely.

---

## 8. Testing and CI/CD

The project includes full automated testing:
- [`tests/`](https://github.com/l3vzNJIT/midterm/tree/master/tests): Unit tests for all plugin commands and shared logic
- [`python-app.yml`](https://github.com/l3vzNJIT/midterm/blob/master/.github/workflows/python-app.yml): GitHub Actions workflow for CI
- [`.coveragerc`](https://github.com/l3vzNJIT/midterm/blob/master/.coveragerc): Configures coverage reporting
- [`pyproject.toml`](https://github.com/l3vzNJIT/midterm/blob/master/pyproject.toml): Specifies project metadata and test dependencies
- [`requirements.txt`](https://github.com/l3vzNJIT/midterm/blob/master/requirements.txt): Lists all Python dependencies including `pandas`, `pytest`, and `python-dotenv`

---

## 9. Commit History and Practices

The [commit history](https://github.com/l3vzNJIT/midterm/commits/master) reflects proper use of Git. Each commit is feature-focused and contains logical changes: adding new commands, improving test coverage, fixing edge case bugs, and organizing the file structure. This auditability is important for collaborative work and continuous integration.

---

## 10. Submission Checklist

| Requirement                                | Complete? |
|-------------------------------------------|-----------|
| Plugin-based REPL                         | ✅        |
| CSV + Pandas History Management           | ✅        |
| Environment Variable Usage                | ✅        |
| Logging via built-in logging module       | ✅        |
| EAFP + LBYL Handling                      | ✅        |
| CI via GitHub Actions                     | ✅        |
| 90%+ Test Coverage                        | 🔄        |
| Clean Commit History                      | ✅        |
| README and Technical Explanation          | ✅        |

