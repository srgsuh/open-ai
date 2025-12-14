"""Package for processing application user's data"""
from .repository import get_by_username, get_statistics, increase_statistics
from .statistics import collect_user_statistics

__all__=["get_by_username", "get_statistics", "collect_user_statistics"]