"""
Base parser for theatre website scraping.

Defines an abstract `BaseParser` class used to extract upcoming show data
from a theatre's "What's On" webpage using BeautifulSoup.

Extensible as needed to accomodate any specific theatre's HTML structure and
unique page layout.
"""

from typing import List
from bs4 import BeautifulSoup, Tag
import pandas as pd
from models.show import Show
from models.theatre import Theatre


class BaseParser:
    """Abstract base class for all theatre parsers"""

    def __init__(self, theatre: Theatre, html_soup: BeautifulSoup):
        """
        Initialize the parser with theatre metadata and parsed HTML.

        Args:
            theatre (Theatre): The theatre metadata object.
            html_soup (BeautifulSoup): Parsed HTML of the theatre's "What's On" page.
        """
        self.theatre = theatre
        self.html_soup = html_soup
        self.selectors = self._load_selectors()

    def extract_shows_from_html(self) -> List[Show]:
        """
        Extract a list of upcoming shows from the HTML content.

        Parses the HTML source using theatre-specific CSS selectors
        and constructs `Show` objects for each detected performance.

        Returns:
            List[Show]: A list of upcoming shows extracted from the theatre.

        Raises:
            RuntimeError: If show elements cannot be selected from the HTML.
            RuntimeError: If any individual show element cannot be parsed.
        """
        shows = []
        try:
            show_elements = self.html_soup.select(self.selectors["Shows"])
        except Exception as e:
            raise RuntimeError(
                f"Error extracting show elements from html for {self.theatre.name}"
            ) from e

        for show_element in show_elements:
            try:
                show = self._extract_show_data(show_element)
            except Exception as e:
                raise RuntimeError(
                    f"Error extracting show data from show_element: {show_element}"
                ) from e

            if show:
                shows.append(show)
        return shows

    def _load_selectors(self) -> pd.Series:
        """
        Load CSS selectors for this theatre from configuration.

        Returns:
            pd.Series: A mapping of selector keys (e.g., Title, Raw_Date) to CSS selectors.

        Raises:
            ValueError: If the configuration file is missing, improperly formatted,
                        or lacks a unique entry for the theatre.
        """
        try:
            selectors_df = pd.read_csv(
                "config/scraping_selectors.csv",
                index_col="Theatre_Name",  # TODO create config/scraping_selectors.csv
            )
        except (FileNotFoundError, KeyError) as e:
            raise ValueError(
                f"Selectors not found for theatre: {self.theatre.name}"
            ) from e

        selectors = selectors_df.loc[self.theatre.name]
        if not isinstance(  # selectors type will be DataFrame if theatres is in a non-unique index
            selectors, pd.Series
        ):
            raise ValueError(
                f"There should only be 1 row for {self.theatre.name} in scraping_selectors.csv"
            )

        return selectors

    def _extract_show_data(self, show_element: Tag) -> Show:
        """
        Extract show data from a single HTML element.

        Args:
            show_element (Tag): A BeautifulSoup tag representing a single show.

        Returns:
            Show: The extracted show data.
        """
        title = self._extract_show_property(show_element, "Title")
        raw_date = self._extract_show_property(show_element, "Raw_Date")
        show_url = self._extract_show_property(show_element, "Show_URL")

        return Show(  # TODO Use true start/end dates rather than raw_date
            theatre=self.theatre.name,
            title=title,
            start_date=raw_date,
            end_date=raw_date,
            link=show_url,
        )

    def _parse_date(self, raw_date: str):  # TODO implement date parser
        """
        Parse a raw date string into structured start and end dates.

        Args:
            raw_date (str): The unstructured date string from the page.

        Returns:
            tuple: (start_date, end_date) once implemented.
        """

    def _extract_show_property(self, show_element: Tag, selector_key: str) -> str:
        """
        Extract a specific property from a show HTML element using a selector.

        Args:
            show_element (Tag): The show element from which to extract the property.
            selector_key (str): The selector key, e.g., "Title", "Raw_Date", or "Show_URL".

        Returns:
            str: The extracted property value.

        Raises:
            RuntimeError: If the selector fails or the expected element/attribute is missing.
        """
        try:
            selected_property = show_element.select_one(self.selectors[selector_key])
        except Exception as e:
            raise RuntimeError(
                f"Error extracting {selector_key} from show_element"
            ) from e

        if selected_property is None:
            raise RuntimeError(f"Failed to capture {selector_key} from show_element")

        if selector_key == "Show_URL":
            selected_property = selected_property.get("href")
            if selected_property is None:
                raise RuntimeError(f"href attribute missing from {selector_key}")
        else:
            selected_property = selected_property.text.strip()

        return str(selected_property)
