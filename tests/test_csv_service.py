"""
test_csv_service

Testing suite for CSVService
"""

import os
import csv
import shutil
from typing import Generator, TypeVar
import pytest
from services.csv_service import CSVService


T = TypeVar("T")

YieldFixture = Generator[T, None, None]


class TestCSVService:
    """Test suite for CSVService class"""

    @pytest.fixture
    def csv_filename(self) -> YieldFixture[str]:
        """Docstring for filename

        :return: example filename
        :rtype: str"""
        os.mkdir("testdir")
        yield "testdir/scraped_shows.csv"
        shutil.rmtree("testdir")

    def test_prepare_csv_creates_file_with_headers(self, csv_filename: str):
        """Test that prepare_csv creates a file with correct headers"""
        CSVService.prepare_csv(csv_filename)

        # Check file exists
        assert os.path.exists(csv_filename)

        # Check headers are correct
        with open(csv_filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == CSVService.FIELD_NAMES
