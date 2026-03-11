# eml-to-md

Convert `.eml` email files to clean, readable Markdown.

Supports **Python 3.9–3.14+** — unlike alternatives that are stuck on older versions.

## Features

- HTML emails → Markdown (headings, bold, links, lists)
- Plain text emails preserved as-is
- Multipart emails handled (prefers HTML part)
- Attachment listing with file sizes
- Pipe-friendly: read from stdin, write to stdout
- Usable as a CLI tool **or** Python library

## Installation

```bash
pip install eml-to-md
```

Or with [pipx](https://pipx.pypa.io/) for isolated CLI usage:

```bash
pipx install eml-to-md
```

## CLI Usage

```bash
# Convert a single file (writes message.md alongside it)
eml2md message.eml

# Batch convert into a folder
eml2md *.eml -o converted/

# Print to terminal
eml2md message.eml --stdout

# Pipe from stdin
cat message.eml | eml2md -

# Check version
eml2md --version
```

## Python API

```python
import eml_to_md

# From a file path
markdown = eml_to_md.convert("message.eml")
print(markdown)

# From a file object
with open("message.eml", "rb") as f:
    markdown = eml_to_md.convert(f)

# Convert and write to disk
out_path = eml_to_md.convert_file("message.eml")
# -> writes message.md, returns Path

# Custom output path
eml_to_md.convert_file("message.eml", output="output/email.md")
```

## Output Format

```markdown
# Subject Line

- **From:** sender@example.com
- **To:** recipient@example.com
- **Date:** Mon, 10 Mar 2026 10:00:00 +0000

---

Email body converted to Markdown...

---

## Attachments

- `document.pdf` (142.3 KB)
- `photo.jpg` (1.2 MB)
```

## Development

```bash
git clone https://github.com/glnarayanan/eml-to-md.git
cd eml-to-md
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'

# Run tests
pytest

# Lint
ruff check src/ tests/
```

## License

[MIT](LICENSE)
