""" Helpers that aren't from a specific category """

from urllib.parse import urlencode


def enum(**enums):
    """Emulate enum type"""
    return type("Enum", (), enums)


def is_drm(stream_type: str) -> bool:
    """Checks if stream has DRM"""
    return stream_type in ["dash+http+widevine", "dash+https+widevine"]


def build_kodi_url(url: str, query: dict) -> str:
    """Converts a dictionary into an HTTP GET query"""
    query_str = urlencode(query)
    return f"{url}?{query_str}"
