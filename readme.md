# Lev's Midterm Project
Lev Zelenin - Web Systems Programming - Keith Williams - Spring 2025

# Video demo
https://youtu.be/n0wInApcZRY

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


## 1. Overview

This project implements a command-line calculator in Python, with a focus on professional software development methodologies. It features a plugin-based architecture utilizing the Command pattern, persistent history management with CSV using pandas, structured logging via the built-in `logging` module, and a modular design conducive to testing and maintenance. Configuration is managed using environment variables, following 12-factor app principles. The project also integrates CI/CD through GitHub Actions.

---

## 2. Summary of Software Engineering Principles Demonstrated

The Python Calculator demonstrates practical application of several core software engineering principles and industry-standard tools. It integrates object-oriented design patterns, system configuration best practices, and a strong focus on test-driven development to ensure maintainability, extensibility, and robustness.

First, the codebase effectively implements the **Command design pattern**. This pattern decouples the execution of specific commands from the REPL loop. Each user input is parsed and routed through the `Invoker`, which scans available plugin commands and dispatches the one whose `scope()` method matches the input. Each command plugin implements an `execute()` method that carries out the actual logic. This separation of responsibility enables easy addition of new features — for example, arithmetic operations like `add`, `subtract`, and `divide` are self-contained Python modules in their respective directories.

The **plugin architecture** further reinforces extensibility and modularity. Commands are dynamically discovered and do not require changes to the core application when new capabilities are introduced. Each resides in its own namespace under `calculator/commands`, keeping logic well-organized. The command dispatcher (`invoker.py`) simply iterates over loaded commands and invokes the appropriate one based on input, embodying both the Strategy and Factory design patterns.

The **REPL (Read-Eval-Print Loop)** pattern is central to the user interface. Implemented in `main.py`, it provides an interactive loop that continuously reads user input, passes it through parsing, routes it to the command logic, and prints output. This structure makes the application intuitive to use while maintaining a clean control flow.

The project also emphasizes the use of **standard tools**. Logging is configured with Python’s built-in `logging` module and defined in a reusable `logging.conf` file. System configuration is handled using environment variables loaded by the `python-dotenv` package, following 12-factor app practices. This allows seamless changes to file paths or logging verbosity without modifying source code.

**Test-driven development (TDD)** is a cornerstone of the project. A comprehensive suite of unit tests in the `tests/` folder validates each plugin and utility. For example, the `history_print` plugin is tested for its ability to correctly load and display historical command usage. The CI/CD pipeline, defined in `.github/workflows/python-app.yml`, automatically runs these tests on every push, ensuring that no regressions are introduced. The `.coveragerc` file and test coverage tools enforce measurable quality.

By combining design patterns, standard tooling, configuration management, and automated testing, this project models real-world software engineering practices. It is not only a calculator but a template for how professional Python applications should be built and maintained.

---

## 3. REPL Command Loop

The REPL loop is initiated by [`main.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py). This script handles environment setup, initializes logging based on the `logging.conf` file, and starts the main input loop. User inputs are passed to the `Invoker` class to determine the appropriate plugin for execution.

---

## 4. Plugin System and Command Pattern

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

## 5. Class Responsibilities

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

## 6. Environment Configuration

Runtime environment setup is handled by:
- [`setup_env.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/setup_env.py): Loads environment variables and prepares paths for logging and history persistence.
- `.env`: A file (excluded from version control) specifying paths, limits, and logging levels.
- The system uses `python-dotenv` to read these variables at startup.

This enables flexible configuration across environments and supports practices like using relative/absolute paths and injecting test-specific variables.

---

## 7. Design Patterns in Use

- **Command Pattern**: Each plugin follows a consistent interface, simplifying dispatch.
- **Factory Pattern**: The `Invoker` behaves like a factory for selecting and executing commands.
- **Strategy Pattern**: Different plugins implement their own logic while conforming to a shared interface.
- **Separation of Concerns**: Configuration, logging, input/output, and plugin logic are modular.

---

## 8. Exception Handling

The code adheres to both:
- **EAFP (Easier to Ask Forgiveness than Permission)**: Most plugin operations attempt actions (like file reads) and catch exceptions.
- **LBYL (Look Before You Leap)**: Used in `setup_env.py` and `history.py` to ensure paths exist and files are readable.

Examples:
- [`main.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/main.py#L18): Handles REPL and top-level exceptions.
- [`history.py`](https://github.com/l3vzNJIT/midterm/blob/master/calculator/commands/history/history.py): Manages file access safely.

---

## 9. Testing and CI/CD

The project includes full automated testing:
- [`tests/`](https://github.com/l3vzNJIT/midterm/tree/master/tests): Unit tests for all plugin commands and shared logic
- [`python-app.yml`](https://github.com/l3vzNJIT/midterm/blob/master/.github/workflows/python-app.yml): GitHub Actions workflow for CI
- [`.coveragerc`](https://github.com/l3vzNJIT/midterm/blob/master/.coveragerc): Configures coverage reporting
- [`pyproject.toml`](https://github.com/l3vzNJIT/midterm/blob/master/pyproject.toml): Specifies project metadata and test dependencies
- [`requirements.txt`](https://github.com/l3vzNJIT/midterm/blob/master/requirements.txt): Lists all Python dependencies including `pandas`, `pytest`, and `python-dotenv`

---

## 10. Commit History and Practices

The [commit history](https://github.com/l3vzNJIT/midterm/commits/master) reflects proper use of Git. Each commit is feature-focused and contains logical changes: adding new commands, improving test coverage, fixing edge case bugs, and organizing the file structure. This auditability is important for collaborative work and continuous integration.

---

## 11. Submission Checklist

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
