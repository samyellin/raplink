from sets import Set

class Album:
    def __init__(self, spotifyId, name):
        self.spotifyId = spotifyId
        self.name = name
        self.tracks = Set()
