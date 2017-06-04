from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

import collector.neo4jDriver as neo4jDriver
import os

application = Flask(__name__)
CORS(application)
driver = neo4jDriver.Neo4jDriver(os.environ["NEO4J_PATH"], os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"])

@application.route('/raplink/api/v1.0/link', methods=['GET'])
def link():
    startArtistId = request.args.get("start")
    endArtistId = request.args.get("end")

    shortestPath = driver.getShortestPath(startArtistId, endArtistId)

    return shortestPath

@application.route('/raplink/api/v1.0/typeahead', methods=['GET'])
def typeahead():
    artist = request.args.get("artist")

    return driver.typeahead(artist)


if __name__ == "__main__":
    application.run()
