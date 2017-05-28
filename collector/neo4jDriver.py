from neo4j.v1 import GraphDatabase, basic_auth, Relationship, Node
import relationship
import artist
import track

import jsonpickle

class Neo4jDriver:
    def __init__(self, driver, neo4j_username, neo4j_password):
        self.driver = GraphDatabase.driver(driver, auth=basic_auth(neo4j_username, neo4j_password))

    def createArtistNode(self, newArtist):
        session = self.driver.session()

        spotifyId = session.run("CREATE (a:Artist {spotifyId: {spotifyId}, name: {name}, popularity: {popularity}, createDate: TIMESTAMP(), modifiedDate: TIMESTAMP(), visited: 0}) RETURN a.spotifyId AS spotifyId",
                    {"spotifyId": newArtist.spotifyId, "name": newArtist.name, "popularity": newArtist.popularity})

        session.close()

        return spotifyId

    def wasArtistVisited(self, targetArtist):
        session = self.driver.session()

        result = session.run("MATCH (a:Artist) WHERE a.spotifyId = {spotifyId} RETURN a.visited",
                                {"spotifyId": targetArtist.spotifyId})
        session.close()

        visited = result.single()["a.visited"]

        if (visited > 0):
            return True
        return False

    def markArtistAsVisited(self, targetArtist):
        session = self.driver.session()

        session.run("MATCH (a:Artist) WHERE a.spotifyId = {spotifyId} SET a.visited = 1",
                    {"spotifyId": targetArtist.spotifyId})

        session.close()

    def createTrackEdge(self, currTrack, currAlbum, currentArtist, currTrackArtist):
        session = self.driver.session()

        spotifyId = session.run("MATCH (a:Artist), (b:Artist) WHERE a.spotifyId={firstId} AND b.spotifyId={secondId}" +
                                "CREATE (a)-[t:track {spotifyId: {trackId}, name: {trackName}, album: {trackAlbum} }]->(b) RETURN t",
                                {"firstId": currentArtist.spotifyId, "secondId": currTrackArtist.spotifyId, "trackName": currTrack.name, "trackAlbum": currAlbum.name, "trackId": currTrack.spotifyId})

        session.close()

        return spotifyId

    def isArtistInGraph(self, currentArtist):

        session = self.driver.session()
        result = session.run("MATCH (a:Artist) WHERE a.spotifyId = {spotifyId} RETURN a.spotifyId AS spotifyId",
                                        {"spotifyId": currentArtist.spotifyId})

        session.close()

        if (result.single() is None):
            return False

        return True

    def isEdgePresent(self, currTrack, firstArtist, secondArtist):

        session = self.driver.session()
        result = session.run("MATCH (a:Artist)-[t:track]-(b:Artist) WHERE a.spotifyId = {firstId} AND b.spotifyId = {secondId} AND t.spotifyId = {trackId} RETURN t",
                                {"firstId": firstArtist.spotifyId, "secondId": secondArtist.spotifyId, "trackId": currTrack.spotifyId})
        session.close()

        if (result.single() is None):
            return False

        return True

    def getArtistFromGraphId(self, graphId):

        session = self.driver.session()
        result = session.run("MATCH (a:Artist) WHERE ID(a)={graphId} RETURN a",
                                {"graphId": graphId})
        session.close()

        artistProps = result.single()['a'].properties

        spotifyId = artistProps['spotifyId']
        name = artistProps['name']
        popularity = artistProps['popularity']

        newArtist = artist.Artist(spotifyId, name, popularity)
        return newArtist


    def getTrackFromRelationship(self, currentRelationship):
        trackProps = currentRelationship.properties
        name = trackProps['name']
        spotifyId = trackProps['spotifyId']

        newTrack = track.Track(spotifyId, name)
        return newTrack

    def getShortestPath(self, startArtist, endArtist):

        session = self.driver.session()

        result = session.run("MATCH (a:Artist {spotifyId: {startId}}), (b:Artist {spotifyId: {endId}}), p=shortestpath((a)-[*..15]-(b)) RETURN p",
                                {"startId": startArtist.spotifyId, "endId":endArtist.spotifyId})

        session.close()

        hydratedPath = []
        sequence = 0
        for path in result:
            finalArtistStartId = path['p'].start.id
            finalArtistEndId = path['p'].end.id
            finalArtistStart = self.getArtistFromGraphId(finalArtistStartId)
            finalArtistEnd = self.getArtistFromGraphId(finalArtistEndId)

            currentArtistStart = finalArtistStart

            for currentRelationship in path['p']:
                firstArtistId = currentRelationship.start
                secondArtistId = currentRelationship.end
                firstArtist = self.getArtistFromGraphId(firstArtistId)
                secondArtist = self.getArtistFromGraphId(secondArtistId)
                connectingTrack = self.getTrackFromRelationship(currentRelationship)

                if (currentArtistStart.spotifyId == firstArtist.spotifyId):
                    newRelationship = relationship.Relationship(firstArtist, secondArtist, connectingTrack, sequence)
                    currentArtistStart = secondArtist
                elif (currentArtistStart.spotifyId == secondArtist.spotifyId):
                    newRelationship = relationship.Relationship(secondArtist, firstArtist, connectingTrack, sequence)
                    currentArtistStart = firstArtist

                hydratedPath.append(newRelationship)
                sequence += 1

        for link in hydratedPath:
            print "Start: " + link.startArtist.name + " End: " + link.endArtist.name + " Track: " + link.connectingTrack.name
        pathJson = jsonpickle.encode(hydratedPath)
        return pathJson
