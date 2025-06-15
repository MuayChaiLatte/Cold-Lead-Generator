"""
test_csv_service

Testing suite for CSVService
"""

import os
import csv
from services.csv_service import CSVService


class TestCSVService:
    """Test suite for CSVService class"""

    def test_prepare_csv_creates_file_with_headers(self, filename: str):
        """Test that prepare_csv creates a file with correct headers"""
        CSVService.prepare_csv(filename)

        # Check file exists
        assert os.path.exists(filename)

        # Check headers are correct
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == CSVService.FIELD_NAMES
