"""Core .eml-to-Markdown conversion logic."""

from __future__ import annotations

import email
import email.policy
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import BinaryIO

import html2text


@dataclass
class Attachment:
    """Represents an email attachment."""

    filename: str
    size: int  # bytes


def _parse_message(source: str | Path | BinaryIO) -> EmailMessage:
    """Parse an email source into an EmailMessage.

    Args:
        source: A file path (str/Path) or an open binary file object.

    Returns:
        Parsed EmailMessage.

    Raises:
        FileNotFoundError: If a path is given and the file doesn't exist.
        ValueError: If the source type is not supported.
    """
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "rb") as f:
            return email.message_from_binary_file(f, policy=email.policy.default)

    if hasattr(source, "read"):
        return email.message_from_binary_file(source, policy=email.policy.default)

    raise ValueError(
        f"Expected a file path or binary file object, got {type(source).__name__}"
    )


def _extract_body(msg: EmailMessage) -> str:
    """Extract the email body, preferring HTML converted to Markdown."""
    html_part: str | None = None
    text_part: str | None = None

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if "attachment" in disposition:
                continue

            if content_type == "text/html" and html_part is None:
                html_part = part.get_content()
            elif content_type == "text/plain" and text_part is None:
                text_part = part.get_content()
    else:
        content_type = msg.get_content_type()
        if content_type == "text/html":
            html_part = msg.get_content()
        elif content_type == "text/plain":
            text_part = msg.get_content()

    if html_part:
        converter = html2text.HTML2Text()
        converter.body_width = 0
        converter.ignore_images = False
        converter.ignore_links = False
        return converter.handle(html_part).strip()

    if text_part:
        return text_part.strip()

    return ""


def _extract_attachments(msg: EmailMessage) -> list[Attachment]:
    """List attachments with their filenames and sizes."""
    attachments: list[Attachment] = []

    if not msg.is_multipart():
        return attachments

    for part in msg.walk():
        disposition = str(part.get("Content-Disposition", ""))
        if "attachment" not in disposition:
            continue

        filename = part.get_filename() or "unnamed"
        payload = part.get_payload(decode=True)
        size = len(payload) if payload else 0
        attachments.append(Attachment(filename=filename, size=size))

    return attachments


def _format_size(size: int) -> str:
    """Human-readable file size."""
    if size >= 1_048_576:
        return f"{size / 1_048_576:.1f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} bytes"


def convert(source: str | Path | BinaryIO) -> str:
    """Convert an .eml email to a Markdown string.

    Args:
        source: A file path (str/Path) or an open binary file object.

    Returns:
        The email rendered as a Markdown string.
    """
    msg = _parse_message(source)

    subject = msg.get("Subject", "(no subject)")
    headers = [
        ("From", msg.get("From", "")),
        ("To", msg.get("To", "")),
        ("CC", msg.get("Cc")),
        ("Reply-To", msg.get("Reply-To")),
        ("Date", msg.get("Date", "")),
    ]

    lines: list[str] = [f"# {subject}", ""]

    for label, value in headers:
        if value:
            lines.append(f"- **{label}:** {value}")

    lines += ["", "---", ""]

    body = _extract_body(msg)
    lines.append(body if body else "*(empty body)*")

    attachments = _extract_attachments(msg)
    if attachments:
        lines += ["", "---", "", "## Attachments", ""]
        for att in attachments:
            lines.append(f"- `{att.filename}` ({_format_size(att.size)})")

    return "\n".join(lines) + "\n"


def convert_file(
    source: str | Path,
    output: str | Path | None = None,
) -> Path:
    """Convert an .eml file and write the result to a .md file.

    Args:
        source: Path to the .eml file.
        output: Output path. Defaults to the same directory with a .md extension.

    Returns:
        Path to the written Markdown file.
    """
    source_path = Path(source)
    md = convert(source_path)

    out_path = source_path.with_suffix(".md") if output is None else Path(output)

    out_path.write_text(md, encoding="utf-8")
    return out_path
