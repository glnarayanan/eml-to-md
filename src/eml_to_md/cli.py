"""Command-line interface for eml-to-md."""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from eml_to_md import __version__
from eml_to_md.converter import convert, convert_file


def main(argv: list[str] | None = None) -> None:
    """Entry point for the ``eml2md`` command."""
    parser = argparse.ArgumentParser(
        prog="eml2md",
        description="Convert .eml email files to clean Markdown.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        help='One or more .eml files (use "-" for stdin)',
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Output directory (default: same as input file)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print to stdout instead of writing files",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args(argv)

    # Collect sources: file paths and/or stdin
    sources: list[tuple[str, str | io.BytesIO]] = []

    for f in args.files:
        if f == "-":
            data = sys.stdin.buffer.read()
            sources.append(("<stdin>", io.BytesIO(data)))
        else:
            sources.append((f, f))

    if not sources:
        if not sys.stdin.isatty():
            data = sys.stdin.buffer.read()
            sources.append(("<stdin>", io.BytesIO(data)))
        else:
            parser.error("No input files. Pass .eml files or pipe via stdin.")

    output_dir = Path(args.output_dir) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    errors = 0
    for label, source in sources:
        try:
            if args.stdout or label == "<stdin>":
                md = convert(source)
                sys.stdout.write(md)
                if len(sources) > 1:
                    sys.stdout.write("\n" + "=" * 60 + "\n\n")
            else:
                path = Path(source) if isinstance(source, str) else None

                if path and not path.exists():
                    print(f"error: {label} not found", file=sys.stderr)
                    errors += 1
                    continue

                if path and path.suffix.lower() != ".eml":
                    print(
                        f"warning: {label} has no .eml extension, "
                        "processing anyway",
                        file=sys.stderr,
                    )

                if output_dir and path:
                    out = output_dir / f"{path.stem}.md"
                    convert_file(path, output=out)
                elif path:
                    out = convert_file(path)
                else:
                    md = convert(source)
                    sys.stdout.write(md)
                    continue

                print(f"  {label} -> {out}")

        except Exception as e:
            print(f"error: {label}: {e}", file=sys.stderr)
            errors += 1

    if errors:
        sys.exit(1)
