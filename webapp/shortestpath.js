function getShortestPath() {
  var startArtist = $('#start').val();
  var endArtist = $('#end').val();

  var pathUrl = 'http://127.0.0.1:5000/raplink/api/v1.0/link?start=' + encodeURI(startArtist) + '&end=' + encodeURI(endArtist);

  $("#playlist").empty();
  $("#playlist").append('<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>')
  $.ajax({
    url: pathUrl,
    success: function(result) {
        var path = JSON.parse(result);
        var nodes = new Array();
        var tracks = new Array();
        path.forEach(function(relationship) {
          var node = new Object();
          var check = 0;
          node.name=relationship.startArtist.name;
          node.spotifyId = relationship.startArtist.spotifyId;
          for (var i = 0;i<nodes.length;++i){
            if (nodes[i].spotifyId == node.spotifyId){
              check = 1;
            }
          }
          if (check == 0) { nodes.push(node);}

          node = new Object();
          check = 0;
          node.name=relationship.endArtist.name;
          node.spotifyId = relationship.endArtist.spotifyId;
          for (var i = 0;i<nodes.length;++i){
            if (nodes[i].spotifyId == node.spotifyId){
              check = 1;
            }
          }
          if (check == 0) { nodes.push(node);}

          var track = new Object();
          track.name = relationship.connectingTrack.name;
          track.spotifyId = relationship.connectingTrack.spotifyId;

          tracks.push(track);
        })

        $("#playlist").empty();
        if (tracks.length == 0) {
          $("#playlist").append("<p>No link found.</p>");
          return;
        }

        tracks.forEach(function(track) {
          var spotifyPlayer = '<iframe src="https://open.spotify.com/embed?uri=spotify:track:' + track.spotifyId + '" width="300" height="80" frameborder="0" allowtransparency="true"></iframe><br>';
          $("#playlist").append(spotifyPlayer);
        })
    },
    error: function() {
      $("#playlist").empty();
      $("#playlist").append('<p>There was an error submitting your request. Please try again.</p>')
    }
  });
}
