import argparse
import shutil
import sys
from pathlib import Path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Copy files sorted by extension.")
    parser.add_argument("source", type=Path, help="source directory")
    parser.add_argument("dest", type=Path, nargs="?", default=Path("dist"),
                        help="destination directory (default: dist)")
    return parser.parse_args(argv)


def unique_path(path: Path) -> Path:
    candidate, n = path, 1
    while candidate.exists():
        candidate = path.with_name(f"{path.stem}_{n}{path.suffix}")
        n += 1
    return candidate


def copy_files(src: Path, dest: Path) -> None:
    try:
        items = list(src.iterdir())
    except OSError as e:
        print(f"Cannot read directory {src}: {e}", file=sys.stderr)
        return

    for item in items:
        try:
            if item.is_dir():
                if item.resolve() != dest.resolve():
                    copy_files(item, dest)
            elif item.is_file():
                ext = item.suffix[1:].lower() or "no_extension"
                target_dir = dest / ext
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, unique_path(target_dir / item.name))
        except OSError as e:
            print(f"Cannot copy {item}: {e}", file=sys.stderr)


def main(argv=None):
    args = parse_args(argv)
    if not args.source.is_dir():
        sys.exit(f"Source directory not found: {args.source}")
    copy_files(args.source, args.dest)
    print(f"Done. Files copied to {args.dest.resolve()}")


if __name__ == "__main__":
    main()
