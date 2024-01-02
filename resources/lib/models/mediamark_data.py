""" Mediamark model module """
from dataclasses import dataclass


@dataclass
class MediamarkData:
    """Wrapper for all data needed for mediamark"""

    user_id: int
    profile_id: str
    media_id: int
    version_id: int
    media_viewing_id: int
    session_id: int
