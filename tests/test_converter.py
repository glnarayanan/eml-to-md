"""Tests for eml_to_md.converter."""

import io

import pytest

from eml_to_md.converter import convert, convert_file


class TestConvertPlainText:
    def test_extracts_subject(self, plain_text_eml):
        md = convert(plain_text_eml)
        assert md.startswith("# Plain text test\n")

    def test_extracts_headers(self, plain_text_eml):
        md = convert(plain_text_eml)
        assert "**From:** alice@example.com" in md
        assert "**To:** bob@example.com" in md
        assert "**Date:**" in md

    def test_extracts_body(self, plain_text_eml):
        md = convert(plain_text_eml)
        assert "This is a plain text email." in md
        assert "Best,\nAlice" in md


class TestConvertHTML:
    def test_converts_html_to_markdown(self, html_body_eml):
        md = convert(html_body_eml)
        assert "**HTML**" in md
        assert "[a link](https://example.com)" in md

    def test_converts_lists(self, html_body_eml):
        md = convert(html_body_eml)
        assert "Item one" in md
        assert "Item two" in md


class TestConvertMultipart:
    def test_prefers_html_over_plain(self, multipart_eml):
        md = convert(multipart_eml)
        # Should contain HTML-converted content, not plain text
        assert "_HTML_" in md
        assert "Plain text fallback" not in md

    def test_includes_cc(self, multipart_eml):
        md = convert(multipart_eml)
        assert "**CC:** carol@example.com" in md


class TestConvertAttachments:
    def test_lists_attachments(self, with_attachments_eml):
        md = convert(with_attachments_eml)
        assert "## Attachments" in md
        assert "`notes.txt`" in md

    def test_body_still_extracted(self, with_attachments_eml):
        md = convert(with_attachments_eml)
        assert "See the attached file." in md


class TestConvertMalformed:
    def test_handles_missing_subject(self, malformed_eml):
        md = convert(malformed_eml)
        assert "# (no subject)" in md

    def test_handles_empty_body(self, malformed_eml):
        md = convert(malformed_eml)
        assert "*(empty body)*" in md


class TestConvertFromBinaryIO:
    def test_accepts_file_object(self, plain_text_eml):
        with open(plain_text_eml, "rb") as f:
            md = convert(f)
        assert "# Plain text test" in md

    def test_accepts_bytes_io(self, plain_text_eml):
        data = plain_text_eml.read_bytes()
        md = convert(io.BytesIO(data))
        assert "# Plain text test" in md


class TestConvertFile:
    def test_writes_md_file(self, plain_text_eml, tmp_path):
        out = convert_file(plain_text_eml, output=tmp_path / "out.md")
        assert out.exists()
        content = out.read_text()
        assert "# Plain text test" in content

    def test_default_output_path(self, plain_text_eml, tmp_path):
        # Copy fixture to tmp so we don't pollute fixtures/
        eml = tmp_path / "email.eml"
        eml.write_bytes(plain_text_eml.read_bytes())
        out = convert_file(eml)
        assert out == tmp_path / "email.md"
        assert out.exists()


class TestConvertErrors:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            convert("/nonexistent/path.eml")

    def test_invalid_source_type(self):
        with pytest.raises(ValueError, match="Expected a file path"):
            convert(12345)
