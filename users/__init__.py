"""Package for processing application user's data"""
from .repository import get_by_username, get_statistics, increase_statistics
from .models import User

__all__=["get_by_username", "User", "get_statistics", "increase_statistics"]