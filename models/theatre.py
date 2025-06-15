from dataclasses import dataclass

@dataclass
class Theatre:
    """Represents a theatre with all its properties"""
    name: str
    link: str
    html_file: str