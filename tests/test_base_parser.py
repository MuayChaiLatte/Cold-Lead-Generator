from typing import List
import csv
import pytest
from bs4 import BeautifulSoup
from models.show import Show
from models.theatre import Theatre
from parsers.base_parser import BaseParser


class TestBaseParser:

    @pytest.fixture
    def theatre(self) -> Theatre:
        return Theatre(
            "Wilton's",
            "https://wiltons.org.uk/whats-on/?category=theatre",
            "mock_html_file",
        )

    @pytest.fixture
    def soup(self) -> BeautifulSoup:
        with open(
            "tests/test_base_parser/wiltons_whats_on.htm", encoding="utf-8"
        ) as fp:
            return BeautifulSoup(fp, "html.parser")

    @pytest.fixture
    def expected_shows(self) -> List[Show]:
        shows = []
        with open(
            "tests/test_base_parser/wiltons_scraped_shows.csv", encoding="utf-8"
        ) as f:
            csv_shows = list(csv.DictReader(f))
        for csv_show in csv_shows:
            show = Show(
                csv_show["Theatre"],
                csv_show["What's On"],
                csv_show["Start Date"],
                csv_show["End Date"],
                csv_show["Link"],
            )
            shows.append(show)
        return shows

    def test_extract_shows_from_html(
        self, theatre: Theatre, soup: BeautifulSoup, expected_shows
    ):
        bp = BaseParser(theatre, soup)
        extracted_shows = bp.extract_shows_from_html()
        assert extracted_shows == expected_shows
