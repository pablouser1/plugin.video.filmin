def enum(**enums):
    return type('Enum', (), enums)

def isDrm(stream_type: str)-> bool:
    return stream_type in ['dash+http+widevine', 'dash+https+widevine']
