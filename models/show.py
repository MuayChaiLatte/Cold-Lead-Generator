"""This module defines the Show class and its CSV conversion method."""

from dataclasses import dataclass


@dataclass
class Show:
    """Represents a theatre show with all its properties"""
    theatre: str
    title: str
    start_date: str
    end_date: str
    link: str

    def to_dict(self) -> dict[str,str]:
        """Convert show to dictionary format for CSV writing"""
        return {
            'Theatre': self.theatre,
            'What\'s On': self.title,
            'Start Date': self.start_date,
            'End Date': self.end_date,
            'Link': self.link
        }
