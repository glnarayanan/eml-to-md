"""eml-to-md - Convert .eml email files to clean Markdown."""

from eml_to_md.converter import Attachment, convert, convert_file

__version__ = "0.1.0"
__all__ = ["Attachment", "convert", "convert_file", "__version__"]
