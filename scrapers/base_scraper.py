from abc import ABC
from models.theatre import Theatre


class BaseScraper(ABC):
    """Abstract base class for all theatre scrapers"""

    def __init__(self, theatre: Theatre):
        self.theatre = theatre
        self.soup = None
