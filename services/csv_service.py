"""
csv_service.py

Provides the CSVService class for handling CSV operations related to show and theatre data.
Includes methods for writing shows to a CSV, reading them into a pandas DataFrame, and
preparing CSV files with the appropriate structure.
"""

import csv
from typing import List
import pandas as pd
from models.show import Show


class CSVService:
    """Service for handling CSV operations"""

    FIELD_NAMES = ["Theatre", "What's On", "Start Date", "End Date", "Link"]

    @classmethod
    def prepare_csv(cls, filename: str):
        """Prepare a new CSV file with headers"""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cls.FIELD_NAMES)
            writer.writeheader()

    @classmethod
    def write_shows_to_csv(cls, filename: str, shows: List[Show]):
        """Write list of shows to CSV file"""
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cls.FIELD_NAMES)
            for show in shows:
                writer.writerow(show.to_dict())

    @classmethod
    def read_shows(cls, filename: str) -> pd.DataFrame:
        """Read shows from CSV file into DataFrame"""
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            # Return empty DataFrame with correct columns if file doesn't exist
            return pd.DataFrame(columns=cls.FIELD_NAMES)

    @classmethod
    def read_theatres(cls, filename: str) -> List[dict[str, str]]:
        """Read theatre configuration from CSV"""
        with open(filename, encoding="utf-8") as f:
            return list(csv.DictReader(f))
