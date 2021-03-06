function getShortestPath() {
  var startArtistId = $('#start').data("spotifyId");
  var endArtistId = $('#end').data("spotifyId");

  if (!endArtistId || !startArtistId) {
    if (!endArtistId) {
      $('#end').val("");
      $('#end-field').removeClass("input--filled")
    }

    if (!startArtistId) {
      $('#start').val("");
      $('#start-field').removeClass("input--filled")
    }
    return;
  }

  if (endArtistId == startArtistId) {
    var uniqueMessage = '<p>Artists must be different.</p>';
    $("#playlist").append(uniqueMessage);
    return;
  }

  var pathUrl = 'http://flask-env.unrhcrvngy.us-west-2.elasticbeanstalk.com/raplink/api/v1.0/link?start=' + encodeURI(startArtistId) + '&end=' + encodeURI(endArtistId);

  $("#playlist").empty();
  $("#playlist").append('<i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>')
  $.ajax({
    url: pathUrl,
    success: function(result) {
        var path = JSON.parse(result);
        var nodes = new Array();
        var tracks = new Array();
        $("#playlist").empty();

        if (path.length == 0) {
          var emptyMessage = '<p>No link found.</p>';
          $("#playlist").append(emptyMessage);
          return;
        }

        path.forEach(function(relationship) {
          var startArtist = new Object();
          startArtist.name=relationship.startArtist.name;
          startArtist.spotifyId = relationship.startArtist.spotifyId;


          var endArtist = new Object();
          endArtist.name=relationship.endArtist.name;
          endArtist.spotifyId = relationship.endArtist.spotifyId;

          var track = new Object();
          track.name = relationship.connectingTrack.name;
          track.spotifyId = relationship.connectingTrack.spotifyId;

          var linkMessage = '<p>' + startArtist.name + ' <i class="fa fa-arrow-right" aria-hidden="true"></i> ' + endArtist.name + '</p>'
          var spotifyPlayer = '<iframe src="https://open.spotify.com/embed?uri=spotify:track:' + track.spotifyId + '" width="600" height="80" frameborder="0" allowtransparency="true"></iframe><br>';
          $("#playlist").append(linkMessage + spotifyPlayer);
        })


    },
    error: function() {
      $("#playlist").empty();
      $("#playlist").append('<p>There was an error submitting your request. Please try again.</p>')
    }
  });
}
