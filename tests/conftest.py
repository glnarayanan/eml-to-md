"""Shared test fixtures."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture()
def plain_text_eml():
    return FIXTURES_DIR / "plain_text.eml"


@pytest.fixture()
def html_body_eml():
    return FIXTURES_DIR / "html_body.eml"


@pytest.fixture()
def multipart_eml():
    return FIXTURES_DIR / "multipart.eml"


@pytest.fixture()
def with_attachments_eml():
    return FIXTURES_DIR / "with_attachments.eml"


@pytest.fixture()
def malformed_eml():
    return FIXTURES_DIR / "malformed.eml"
