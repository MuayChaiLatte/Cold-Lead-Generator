import requests
from bs4 import BeautifulSoup
from models.theatre import Theatre


class TheatreWebsiteScraper:
    """Retrieves HTML source file via HTTP request to Theatre Website"""

    def __init__(self, theatre: Theatre):
        self.theatre = theatre
        self.soup = None

    def _get_soup(self) -> BeautifulSoup:
        """Retrieve object from http request to theatre website"""
        try:
            response = requests.get(self.theatre.link, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch {self.theatre.link}: {e}") from e

    def get_html(
        self, is_using_static_html: bool = False, static_html_file: str = "test.html"
    ) -> BeautifulSoup:
        """Returns html source file for theatre

        Args:
            is_using_static_html (bool, optional): controls run-mode for testing with a static pre-downloaded file. Defaults to False.
            static_html_file (str, optional): static pre-downloaded file for testing. Defaults to "test.html".

        Returns:
            BeautifulSoup: _description_
        """
        if is_using_static_html:
            self.soup = BeautifulSoup(static_html_file, "html.parser")
        else:
            self.soup = self._get_soup()
        return self.soup
