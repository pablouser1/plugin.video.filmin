""" Headers helper """

from requests import Session


class Headers:
    """Common Filmin headers"""

    DEVICE_MODEL = "Kodi"
    DEVICE_OS_VERSION = "15"
    CLIENT_VERSION = "5.20.1"

    @staticmethod
    def set_new(session: Session):
        """
        Updates session headers with X-* keys
        Used in both apiv3 and uapi
        """

        session.headers.update({
            "X-Client-Version": Headers.CLIENT_VERSION,
            "X-Device-Model": Headers.DEVICE_MODEL,
            "X-Device-OS-Version": Headers.DEVICE_OS_VERSION,
        })

    @staticmethod
    def set_old(session: Session):
        """
        Updates session headers with old keys
        Used for mediamark, apiv3 and uapi
        """

        session.headers.update({
            "clientversion": Headers.CLIENT_VERSION,
            "devicemodel": Headers.DEVICE_MODEL,
            "deviceosversion": Headers.DEVICE_OS_VERSION,
        })

    @staticmethod
    def set_common(session: Session, lang: str):
        """Updates session headers with keys common for both old and new"""
        session.headers.update({
            "clientlanguage": lang
        })
