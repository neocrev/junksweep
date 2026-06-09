import os
import sys
import shutil
import argparse
import textwrap
from pathlib import Path

JUNK_NAMES = {
    "node_modules",
    "__pycache__",
    ".git",
    ".next",
    ".nuxt",
    "build",
    "dist",
    "target",
    ".cache",
    ".parcel-cache",
    ".turbo",
    ".svelte-kit",
    "vendor/bundle",
    "Pods",
    ".gradle",
    "go/pkg/mod",
    "elm-stuff",
    "_build",
    "deps",
    "CMakeFiles",
    ".tox",
    ".eggs",
    "*.egg-info",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".serverless",
}

HUMAN_READABLE = {
    "node_modules": "Node.js dependencies",
    "__pycache__": "Python bytecode cache",
    ".git": "Git repository data",
    ".next": "Next.js build output",
    ".nuxt": "Nuxt.js build output",
    "build": "Build artifacts",
    "dist": "Distribution bundles",
    "target": "Rust/Java build output",
    ".cache": "Cache files",
    ".turbo": "Turborepo cache",
    "Pods": "CocoaPods dependencies",
    ".gradle": "Gradle cache",
}


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T"):
        if abs(num) < 1024.0:
            return f"{num:>7.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:>7.1f}P{suffix}"


def get_dir_size(path, follow_symlinks=False):
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=follow_symlinks):
                    total += get_dir_size(entry.path, follow_symlinks)
                elif entry.is_file(follow_symlinks=follow_symlinks):
                    total += entry.stat(follow_symlinks=follow_symlinks).st_size
            except (PermissionError, OSError):
                pass
    except (PermissionError, OSError):
        pass
    return total


def scan(root, depth=3, min_size_mb=1):
    root = Path(root).resolve()
    results = []
    junk_set = set(name.replace("/", os.sep) for name in JUNK_NAMES)

    for dirpath, dirnames, _ in os.walk(root, followlinks=False):
        rel = Path(dirpath).relative_to(root)
        parts = rel.parts

        if len(parts) > depth:
            dirnames.clear()
            continue

        for name in list(dirnames):
            full = os.path.join(dirpath, name)
            rel_path = str(Path(rel) / name) if str(rel) != "." else name
            parts_lower = set(p.lower() for p in Path(rel_path).parts)

            match = name in junk_set
            if not match:
                # Also check folder names that appear as just the junk name
                for junk in junk_set:
                    junk_parts = junk.replace("\\", "/").split("/")
                    if len(junk_parts) == 1 and name.lower() == junk_parts[0].lower():
                        match = True
                        break

            if match:
                size = get_dir_size(full)
                if size >= min_size_mb * 1024 * 1024:
                    results.append({
                        "path": full,
                        "size": size,
                        "name": name,
                        "rel": rel_path,
                    })

    results.sort(key=lambda x: x["size"], reverse=True)
    return results


def print_results(results):
    if not results:
        print("✨ No junk found!")
        return

    total = sum(r["size"] for r in results)
    print(f"\n{'SIZE':>10}  {'DIR':<8}  PATH")
    print(f"{'─'*10}  {'─'*8}  {'─'*50}")
    for r in results:
        label = HUMAN_READABLE.get(r["name"], r["name"])
        print(f"{sizeof_fmt(r['size'])}  {label:<8}  {r['rel']}")
    print(f"\n{'─'*70}")
    print(f"{'Total':>10}: {sizeof_fmt(total)} across {len(results)} directories")


def confirm_clean(results, dry_run):
    if not results:
        return

    print()
    resp = input(f"Remove {len(results)} directories ({sizeof_fmt(sum(r['size'] for r in results))})? [y/N/a(ll)/?] ").strip().lower()

    if resp == "?":
        print()
        for i, r in enumerate(results, 1):
            print(f"  {i:>3}. {sizeof_fmt(r['size'])}  {r['rel']}")
        return confirm_clean(results, dry_run)

    if resp == "a":
        resp = "y"

    if resp != "y":
        print("Aborted.")
        return

    removed = 0
    failed = 0
    for r in results:
        try:
            if not dry_run:
                shutil.rmtree(r["path"])
            removed += 1
        except PermissionError as e:
            print(f"  ✗ Permission denied: {r['rel']}")
            failed += 1

    print(f"\n  ✓ Removed {removed} directories ({sizeof_fmt(sum(r['size'] for r in results))})")
    if failed:
        print(f"  ✗ {failed} failed (permission denied)")


def main():
    parser = argparse.ArgumentParser(
        prog="junksweep",
        description="Find and clean junk directories (node_modules, __pycache__, .git, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              junksweep                          Scan current directory
              junksweep ~/projects                Scan specific path
              junksweep --clean                   Scan + prompt to delete
              junksweep --dry-run                 Show what would be deleted
              junksweep --depth 5                 Scan deeper (default: 3)
              junksweep --min-size 10             Only show dirs >= 10MB
        """),
    )
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--clean", "-c", action="store_true", help="Prompt to delete found junk")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Show what would be deleted")
    parser.add_argument("--depth", type=int, default=3, help="Max scan depth (default: 3)")
    parser.add_argument("--min-size", type=int, default=1, help="Min size in MB (default: 1)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    results = scan(args.path, args.depth, args.min_size)

    if args.json:
        import json
        data = [{"path": r["path"], "size": r["size"], "name": r["name"]} for r in results]
        data.append({"total_size": sum(r["size"] for r in results), "count": len(results)})
        json.dump(data, sys.stdout, indent=2)
        print()
        return

    print_results(results)

    if args.clean or args.dry_run:
        confirm_clean(results, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
