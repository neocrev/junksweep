# junksweep

**Find and clean junk directories — reclaim gigabytes.**

A fast CLI tool that scans your projects for `node_modules`, `__pycache__`, `.git`, `target`, `build`, and other junk directories, shows how much space they waste, and optionally removes them.

```bash
pip install junksweep
junksweep ~/projects --clean
```

## Why?

- `node_modules` can be gigabytes per project
- `__pycache__` and `.ruff_cache` pile up silently
- Rust `target/` directories are huge
- `.next`, `build`, `dist` take space after CI

One command to see it all. One prompt to clean it up.

## Install

```bash
pip install junksweep
```

## Usage

```bash
# Scan current directory
junksweep

# Scan a specific path
junksweep ~/projects

# Scan + prompt to delete
junksweep --clean

# Dry run (show what would be deleted)
junksweep ~/projects --dry-run

# Scan deeper (default: 3 levels)
junksweep --depth 5

# Only show dirs >= 50MB
junksweep --min-size 50

# Machine-readable output
junksweep --json
```

## Default junk list

`node_modules`, `__pycache__`, `.git`, `.next`, `.nuxt`, `build`, `dist`, `target`, `.cache`, `.turbo`, `Pods`, `.gradle`, `vendor/bundle`, `elm-stuff`, `deps`, `CMakeFiles`, `.tox`, `.eggs`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `.serverless` and more.

## Output example

```
      SIZE    DIR       PATH
──────────  ────────  ──────────────────────────────────────
  1.2GiB    node_modules  my-app/node_modules
340.0MiB    .next         webapp/.next
245.0MiB    target        rust-service/target
 42.0MiB    build         electron-app/build
 12.3MiB    __pycache__   api/__pycache__

──────────────────────────────────────────────────────────────
     Total:  1.8GiB across 5 directories
```

## License

MIT
