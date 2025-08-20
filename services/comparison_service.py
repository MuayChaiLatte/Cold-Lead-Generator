import pandas as pd
from typing import List
from models.show import Show


class ComparisonService:
    """Service for comparing show lists and finding new shows"""

    @staticmethod
    def find_new_shows(
        current_shows: List[Show], previous_shows: pd.DataFrame
    ) -> List[Show]:
        """Find shows that are new compared to previous scraping"""
        new_shows = []

        for show in current_shows:
            if ComparisonService._is_new_show(show, previous_shows):
                new_shows.append(show)

        return new_shows

    @staticmethod
    def _is_new_show(show: Show, previous_shows: pd.DataFrame) -> bool:
        """Check if a show is new (not in previous shows)"""
        if previous_shows.empty:
            return True

        matching_rows = (
            (previous_shows["Theatre"] == show.theatre)
            & (previous_shows["What's On"] == show.title)
            & (previous_shows["Start Date"] == show.start_date)
            & (previous_shows["End Date"] == show.end_date)
        )

        return not matching_rows.any()
