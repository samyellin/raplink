import requests
import urllib
import sys
from sets import Set
import artist
import album
import track
import neo4jDriver

class Collector:

    def __init__(self):
        self.spotifyApiBase = "https://api.spotify.com/v1/"
        self.spotifyApiSearch = self.spotifyApiBase + "search?q="
        self.spotifyApiArtist = self.spotifyApiBase + "artists/"
        self.spotifyApiAlbum = self.spotifyApiBase + "albums/"
        self.graphDbDriver = neo4jDriver.Neo4jDriver("bolt://ec2-52-10-102-229.us-west-2.compute.amazonaws.com:7687", "neo4j", "test")
        self.artistStack = []

    def initiateCrawl(self, artistSeed):
        initialArtist = self.getSeedArtist(artistSeed)
        if not (self.graphDbDriver.isArtistInGraph(initialArtist)):
            self.graphDbDriver.createArtistNode(initialArtist)
        self.artistStack.append(initialArtist)
        self.discover()

    def getSeedArtist(self, artistSeed):
        encodedArtistSeed = urllib.quote_plus(artistSeed)
        search = self.spotifyApiSearch + encodedArtistSeed + "&type=artist"

        r = requests.get(search)
        seedArtistJson = r.json()
        seedArtistId = seedArtistJson['artists']['items'][0]['id']
        newArtist = self.getArtistFromSpotifyId(seedArtistId)
        return newArtist

    def getArtistFromSpotifyId(self, spotifyId):
        artistUrl = self.spotifyApiArtist + spotifyId
        r = requests.get(artistUrl)
        artistJson = r.json()
        newArtist = self.constructArtistFromSpotifyJson(artistJson)
        albums = self.getArtistAlbums(newArtist)
        newArtist.initializeAlbums(albums)
        return newArtist

    def getArtistAlbums(self, selectedArtist):
        artistSpotifyId = selectedArtist.spotifyId
        spotifyApiArtistAlbumsUrl = self.spotifyApiArtist + artistSpotifyId + "/albums"
        try:
            r = requests.get(spotifyApiArtistAlbumsUrl)
            artistAlbumsJson = r.json()
            artistAlbums = self.constructAlbumsFromSpofityJson(artistAlbumsJson)
        except:
            print("Error fetching albums for " + selectedArtist.name)
            artistAlbums = []
        return artistAlbums

    def constructArtistFromSpotifyJson(self, json):
        try:
            artistName = json['name']
            artistId = json['id']
            artistPopularity = json['popularity']
            newArtist = artist.Artist(artistId, artistName, artistPopularity)
        except:
            print(json)
            sys.exit(1)
        return newArtist

    def constructAlbumsFromSpofityJson(self, json):
        albums = Set()
        for currAlbum in json['items']:
            albumName = currAlbum['name']
            albumId = currAlbum['id']
            newAlbum = album.Album(albumId, albumName)
            albums.add(newAlbum)
        return albums

    def constructTracksFromSpotifyJson(self, json):
        tracks = Set()
        for currTrack in json['tracks']['items']:
            currTrackSpotifyId = currTrack['id']
            currTrackName = currTrack['name']
            newTrack = track.Track(currTrackSpotifyId, currTrackName)
            artists = Set()
            for currArtist in currTrack['artists']:
                artistId = currArtist['id']
                newArtist = self.getArtistFromSpotifyId(artistId)
                newArtistAlbums = self.getArtistAlbums(newArtist)
                newArtist.initializeAlbums(newArtistAlbums)
                artists.add(newArtist)
            newTrack.initializeArtists(artists)
            tracks.add(newTrack)
        return tracks

    def getTracksForAlbum(self, currAlbum):
        trackUrl = self.spotifyApiAlbum + currAlbum.spotifyId
        r = requests.get(trackUrl)
        tracksJson = r.json()
        albumTracks = self.constructTracksFromSpotifyJson(tracksJson)
        return albumTracks

    def addArtistToStack(self, nextArtist):
        for waitingArtist in self.artistStack:
            if (waitingArtist.spotifyId == nextArtist.spotifyId):
                return
        print("Adding " + nextArtist.name + " to stack.")
        self.artistStack.append(nextArtist)

    def discover(self):
        currentArtist = self.artistStack.pop()
        if (self.graphDbDriver.wasArtistVisited(currentArtist) is False):
            self.graphDbDriver.markArtistAsVisited(currentArtist)
            print("\n\n\n")
            print("Artist: " + currentArtist.name)
            for currAlbum in currentArtist.albums:
                tracks = self.getTracksForAlbum(currAlbum)
                print("Album: " + currAlbum.name)
                for currTrack in tracks:
                    print("Track: " + currTrack.name)
                    for currTrackArtist in currTrack.artists:
                        if (self.graphDbDriver.isArtistInGraph(currTrackArtist) is False):
                            print("Creating Artist: " + currTrackArtist.name)
                            self.graphDbDriver.createArtistNode(currTrackArtist)
                            if (currTrackArtist.popularity > 70):
                                self.addArtistToStack(currTrackArtist)
                        if (currTrackArtist.popularity > 70 and (self.graphDbDriver.wasArtistVisited(currTrackArtist) is False)):
                            self.addArtistToStack(currTrackArtist)

                        for targetArtist in currTrack.artists:
                            if (currTrackArtist != targetArtist and not self.graphDbDriver.isEdgePresent(currTrack, targetArtist, currTrackArtist)):
                                print("Edge: " + targetArtist.name + " <-> " + currTrackArtist.name + ", " + currTrack.name)
                                self.graphDbDriver.createTrackEdge(currTrack, currAlbum, targetArtist, currTrackArtist)
        else:
            print("\n"+currentArtist.name + " was already visited.")
        if len(self.artistStack) == 0:
            return
        self.discover()
