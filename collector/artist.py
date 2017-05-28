from sets import Set

class Artist:

    def __init__(self, spotifyId, name, popularity):
            self.spotifyId = spotifyId
            self.name = name
            self.popularity = popularity
            self.albums = Set()

    def initializeAlbums(self, albumSet):
        self.albums = albumSet
