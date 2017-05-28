from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin

import collector.collector as collector
import collector.neo4jDriver as neo4jDriver

app = Flask(__name__)
CORS(app)
driver = neo4jDriver.Neo4jDriver("bolt://ec2-52-10-102-229.us-west-2.compute.amazonaws.com:7687", "neo4j", "test")

@app.route('/raplink/api/v1.0/link', methods=['GET'])
def crawl():

    startArtist = request.args.get("start")
    endArtist = request.args.get("end")

    spotifyCollector = collector.Collector()

    shortestPath = driver.getShortestPath(spotifyCollector.getSeedArtist(startArtist), spotifyCollector.getSeedArtist(endArtist))

    return shortestPath

if __name__ == "__main__":
    app.run()
