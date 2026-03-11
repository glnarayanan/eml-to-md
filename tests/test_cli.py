"""Tests for eml_to_md.cli."""

from pathlib import Path

import pytest

from eml_to_md.cli import main

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestCLIStdout:
    def test_stdout_flag(self, plain_text_eml, capsys):
        main([str(plain_text_eml), "--stdout"])
        captured = capsys.readouterr()
        assert "# Plain text test" in captured.out

    def test_multiple_files_stdout(self, plain_text_eml, html_body_eml, capsys):
        main([str(plain_text_eml), str(html_body_eml), "--stdout"])
        captured = capsys.readouterr()
        assert "# Plain text test" in captured.out
        assert "# HTML email test" in captured.out
        assert "=" * 60 in captured.out


class TestCLIFileOutput:
    def test_writes_md_file(self, plain_text_eml, tmp_path):
        eml = tmp_path / "msg.eml"
        eml.write_bytes(plain_text_eml.read_bytes())
        main([str(eml)])
        assert (tmp_path / "msg.md").exists()

    def test_output_dir_flag(self, plain_text_eml, tmp_path):
        out_dir = tmp_path / "output"
        main([str(plain_text_eml), "-o", str(out_dir)])
        assert (out_dir / "plain_text.md").exists()


class TestCLIErrors:
    def test_missing_file(self, capsys):
        with pytest.raises(SystemExit, match="1"):
            main(["/nonexistent/file.eml"])
        captured = capsys.readouterr()
        assert "not found" in captured.err

    def test_no_args_tty(self, monkeypatch):
        monkeypatch.setattr("sys.stdin", open("/dev/null"))  # noqa: SIM115
        monkeypatch.setattr("sys.stdin.isatty", lambda: True)
        with pytest.raises(SystemExit, match="2"):
            main([])


class TestCLIVersion:
    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit, match="0"):
            main(["-V"])
        captured = capsys.readouterr()
        assert "eml2md" in captured.out
        assert "0.1.0" in captured.out


class TestCLIStdin:
    def test_dash_reads_stdin(self, plain_text_eml, monkeypatch, capsys):
        data = plain_text_eml.read_bytes()
        import io

        monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(data)))
        main(["-"])
        captured = capsys.readouterr()
        assert "# Plain text test" in captured.out
