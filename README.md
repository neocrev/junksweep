# junksweep

One command to see how much of your disk is `node_modules` and `__pycache__`. One prompt to clean it up.

```bash
pip install junksweep
junksweep ~/projects --clean
```

I had 14 `node_modules` directories on my laptop. Combined they were larger than my Steam library. This is that problem in a command.

## What it finds

```
      SIZE    DIR            PATH
──────────  ──────────────  ──────────────────────────
  1.2GiB    node_modules    my-app/node_modules
340.0MiB    .next           webapp/.next
245.0MiB    target          rust-service/target
 42.0MiB    build           electron-app/build
 12.3MiB    __pycache__     api/__pycache__

──────────────────────────────────────────────────────
     Total:  1.8GiB across 5 directories
```

It knows about `node_modules`, `__pycache__`, `.git`, `.next`, `build`, `dist`, `target`, `Pods`, `.gradle`, `vendor/bundle`, `elm-stuff`, `.tox`, `.mypy_cache`, `.ruff_cache`, and about 20 more.

## Usage

```bash
# Scan current directory
junksweep

# Scan a specific path
junksweep ~/projects

# Scan + prompt to delete
junksweep --clean

# Don't actually delete, just show me
junksweep ~/projects --dry-run

# Dig deeper
junksweep --depth 5

# Only show the big stuff (>= 50MB)
junksweep --min-size 50

# Machine-readable
junksweep --json
```

## Install

```bash
pip install junksweep
```

Python 3.8+, no dependencies.

## License

MIT
