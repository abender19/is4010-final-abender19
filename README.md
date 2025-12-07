# File Statistics Analyzer

[![Tests](https://github.com/abender19/is4010-final-abender19/actions/workflows/tests.yml/badge.svg)](https://github.com/abender19/is4010-final-abender19/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A command-line tool for analyzing files and directories. Get detailed statistics about file types, sizes, line counts, and more.

## Features

- **File Analysis**: Get detailed statistics for individual files (size, line count, type)
- **Directory Analysis**: Analyze entire directory trees with recursive scanning
- **File Type Distribution**: See breakdown of file types in directories
- **Size Summary**: Get total sizes in bytes, KB, and MB
- **Largest Files**: Identify the 5 largest files in a directory
- **Line Counting**: Count total lines of code/text across files
- **Error Handling**: Graceful handling of permission errors, missing files, and binary content
- **Rich Output**: Beautiful, formatted terminal output using Rich library

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/abender19/is4010-final-abender19.git
cd is4010-final-abender19
```

2. Install in development mode with dependencies:
```bash
pip install -e ".[dev]"
```

Or install just the runtime dependencies:
```bash
pip install -e .
```

## Usage

### Analyze a single file

```bash
filestat path/to/file.txt
```

**Example output:**
```
File Analysis: file.txt

File Statistics
┏━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Property   ┃ Value    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━┩
│ File Name  │ file.txt │
│ Size (by…  │ 1024     │
│ Size (KB)  │ 1.0      │
│ File Type  │ .txt     │
│ Lines      │ 25       │
└────────────┴──────────┘
```

### Analyze a directory

```bash
filestat path/to/directory
```

**Example output:**
```
Directory Analysis

Summary
┏━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric         ┃ Value ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Files    │ 42    │
│ Total Direct…  │ 5     │
│ Total Size …   │ 50240 │
│ Total Size …   │ 49.06 │
│ Total Size …   │ 0.05  │
│ Total Lines …  │ 1500  │
└────────────────┴───────┘

File Types
┏━━━━━━━━━┳━━━━━━┓
┃ Extensi… ┃ Count ┃
┡━━━━━━━━━╇━━━━━━┩
│ .py     │ 15   │
│ .txt    │ 12   │
│ .json   │ 10   │
│ .md     │ 5    │
└─────────┴──────┘

Largest Files
┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ File Name  ┃ Size … ┃ Path    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│ large.py   │ 5.12   │ large… │
│ script.py  │ 3.07   │ src/s… │
└────────────┴────────┴─────────┘
```

### Analyze current directory

```bash
filestat .
```

### Get help

```bash
filestat --help
```

## Testing

Run the test suite locally:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ -v --cov=filestat --cov-report=html
```

View the coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Coverage

The project includes comprehensive tests covering:

- **File Analysis**: Single file statistics, line counting, size calculations
- **Directory Analysis**: Recursive scanning, file type distribution, largest file detection
- **Error Handling**: Missing files, permission errors, binary files
- **CLI**: Argument parsing, help text, exit codes
- **Formatting**: Output formatting for both file and directory statistics

**Total Tests**: 25+ covering all major features and edge cases

## Project Structure

```
is4010-final-abender19/
├── filestat/                    # Main package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for python -m filestat
│   ├── analyzer.py             # Core analysis logic (FileAnalyzer class)
│   ├── formatter.py            # Output formatting (rich tables)
│   └── cli.py                  # CLI argument parsing and main()
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_analyzer.py        # Tests for FileAnalyzer
│   ├── test_formatter.py       # Tests for formatting
│   └── test_cli.py             # Tests for CLI
├── .github/workflows/
│   └── tests.yml               # GitHub Actions CI/CD workflow
├── pyproject.toml              # Project configuration (PEP 517/518)
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── LICENSE                     # MIT License
└── AGENTS.md                   # AI-assisted development documentation
```

## Technical Stack

- **Language**: Python 3.10+
- **CLI Framework**: argparse (standard library)
- **Output Formatting**: Rich (for beautiful terminal tables)
- **Testing**: pytest with pytest-cov
- **CI/CD**: GitHub Actions
- **Package Management**: pip with pyproject.toml (PEP 517/518)

## GitHub Actions CI/CD

This project uses GitHub Actions to automatically run tests on every push to main. The workflow:

1. Tests on Python 3.10, 3.11, and 3.12
2. Installs dependencies from pyproject.toml
3. Runs pytest with coverage reporting
4. Uploads coverage to Codecov

View the workflow status in the [Actions Tab](https://github.com/abender19/is4010-final-abender19/actions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## AI-Assisted Development

This project was developed with assistance from AI tools including GitHub Copilot and Claude. For details on how AI was used throughout the development process, see [AGENTS.md](AGENTS.md).

## Author

**Alec Bender**

- GitHub: [@abender19](https://github.com/abender19)
- Repository: [is4010-final-abender19](https://github.com/abender19/is4010-final-abender19)
