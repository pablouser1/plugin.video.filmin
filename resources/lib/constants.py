def __enum(**enums):
    return type('Enum', (), enums)

ROUTES = __enum(
    HOME='home',
    CATALOG='catalog',
    SEARCH='search',
    PURCHASED='purchased',
    WATCHING='watching',
    HIGHLIGHTEDS='highlighteds',
    PLAYLISTS='playlists',
    PLAYLIST='playlist',
    COLLECTIONS='collections',
    COLLECTION='collection',
    SEASONS='seasons',
    EPISODES='episodes',
    PLAYER='player'
)
