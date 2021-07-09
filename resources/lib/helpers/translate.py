from ..common import env
def translate(translation_id: int):
    result = env.getAddon().getLocalizedString(translation_id)
    return result
