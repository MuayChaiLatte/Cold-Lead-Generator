from datetime import datetime
from dateutil.parser import parse as parse_date


class DateUtils:
    """Utility class for date operations"""

    @staticmethod
    def get_current_year() -> str:
        """Get current year as string"""
        return str(datetime.today().year)

    @staticmethod
    def format_dates(start_date: str, end_date: str) -> tuple[str, str]:
        """Format dates to YYYY-MM-DD format"""
        start_formatted = parse_date(start_date).strftime("%Y-%m-%d")
        end_formatted = parse_date(end_date).strftime("%Y-%m-%d")
        return start_formatted, end_formatted
