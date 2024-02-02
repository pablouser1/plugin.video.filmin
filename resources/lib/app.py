""" Module entrypoint """

from .routes import dispatch
from .session import ask_login, ask_domain
from .common import settings, api, _PARAMS


def run():
    """App entrypoint"""

    # Check if user already has a session, ask for credentials if not
    if settings.is_logged_in():
        token_info = settings.get_auth()
        profile_id = settings.get_profile_id()
        api.set_token(token_info["access"])
        api.set_profile_id(profile_id)
    else:
        ask_domain()
        ask_login()

    # Run view
    dispatch(_PARAMS)
