"""
Any path decorated with the limiter _must_ take a parameter `fastapi.Request`
in order for the limiter to operate.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address


limiter = Limiter(key_func=get_remote_address)
