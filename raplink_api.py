from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

import collector.collector as collector
import collector.neo4jDriver as neo4jDriver
import os

app = Flask(__name__)
CORS(app)
driver = neo4jDriver.Neo4jDriver(os.environ["NEO4J_PATH"], os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])

@app.route('/raplink/api/v1.0/link', methods=['GET'])
def crawl():
    startArtist = request.args.get("start")
    endArtist = request.args.get("end")

    spotifyCollector = collector.Collector()

    shortestPath = driver.getShortestPath(spotifyCollector.getSeedArtist(startArtist), spotifyCollector.getSeedArtist(endArtist))

    return shortestPath

@app.route('/raplink/api/v1.0/typeahead', methods=['GET'])
def typeahead():
    artist = request.args.get("artist")

    return driver.typeahead(artist)


if __name__ == "__main__":
    app.run()
