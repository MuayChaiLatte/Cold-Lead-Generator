from abc import ABC
from models.theatre import Theatre
import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """Abstract base class for all theatre scrapers"""

    def __init__(self, theatre: Theatre):
        self.theatre = theatre
        self.soup = None

    def _get_soup(self) -> BeautifulSoup:
        """Get BeautifulSoup object from http request to theatre website"""
        try:
            response = requests.get(self.theatre.link, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch {self.theatre.link}: {e}") from e
