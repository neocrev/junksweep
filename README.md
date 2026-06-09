# junksweep

[![PyPI](https://img.shields.io/pypi/v/junksweep)](https://pypi.org/project/junksweep/) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Find out how much of your disk is `node_modules` and `__pycache__`. Then clean it up.

<p align="center">
  <img src="demo.svg" alt="junksweep in action" width="620">
</p>

---

## Quick start

```bash
pip install junksweep

# Scan current directory
junksweep

# Scan + prompt to delete
junksweep ~/projects --clean
```

---

## Usage

```bash
# Scan a specific path
junksweep ~/projects

# Don't actually delete
junksweep --dry-run

# Dig deeper
junksweep --depth 5

# Only show big stuff (>= 50MB)
junksweep --min-size 50

# Machine-readable output
junksweep --json
```

---

## What it detects

`node_modules`, `__pycache__`, `.git`, `.next`, `build`, `dist`, `target`, `Pods`, `.gradle`, `vendor/bundle`, `elm-stuff`, `.tox`, `.mypy_cache`, `.ruff_cache` — and about 20 more.

Python 3.8+, no dependencies.

---

## License

MIT
