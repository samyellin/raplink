from sets import Set

class Track:

    def __init__(self, spotifyId, name):
            self.spotifyId = spotifyId
            self.name = name
            self.artists = Set()

    def initializeArtists(self, artistSet):
        self.artists = artistSet
