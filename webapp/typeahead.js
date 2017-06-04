$(function() {

  typeaheadResultHandler = function(ul, item) {
    var connectedIcon;
    if (item.connected) {
      connectedIcon = '<i class="fa fa-check-square" aria-hidden="true"></i>'
    } else {
      connectedIcon = '<i class="fa fa-window-close" aria-hidden="true"></i>'
    }
    return $( "<li>" )
      .append( '<div class=typeahead-item>' + item.name + " " + connectedIcon + "</div>")
      .appendTo( ul );
  };

  $( "#start" ).autocomplete({
    source: function( request, response ) {
      var typeaheadUrl = 'http://flask-env.unrhcrvngy.us-west-2.elasticbeanstalk.com/raplink/api/v1.0/typeahead?artist=' + encodeURI($("#start").val());
      $.ajax({
        url: typeaheadUrl,
        success: function( data ) {
          response( JSON.parse(data) );
        }
      });
    },
    select: function( event, ui ) {
      $( "#start" ).val( ui.item.name );
      $( "#start" ).data("spotifyId", ui.item.spotifyId);
      $( "#start-field" ).addClass("input--filled");
      getShortestPath();
      return false;
    },
    minLength: 1
  })
  .autocomplete( "instance" )._renderItem = typeaheadResultHandler;

  $( "#end" ).autocomplete({
    source: function( request, response ) {
      var typeaheadUrl = 'http://flask-env.unrhcrvngy.us-west-2.elasticbeanstalk.com/raplink/api/v1.0/typeahead?artist=' + encodeURI($("#end").val());
      $.ajax({
        url: typeaheadUrl,
        success: function( data ) {
          response( JSON.parse(data) );
        }
      });
    },
    select: function( event, ui ) {
      $( "#end" ).val( ui.item.name );
      $( "#end" ).data("spotifyId", ui.item.spotifyId);
      $( "#end-field" ).addClass("input--filled");
      getShortestPath();
      return false;
    },
    minLength: 1
  })
  .autocomplete( "instance" )._renderItem = typeaheadResultHandler;

  // Detectors on input
  $("#start").change(function(){
    if ($("#start").data("spotifyId") && $("#start").data("spotifyId") != "" && $("#start").val() != "") {
      $("#start-field").addClass("input--filled");
    } else {
      $("#start").val("")
      $('#start').data("spotifyId", "");
      $("#start-field").removeClass("input--filled");
    }
  })
  $("#end").change(function(){
    if ($("#end").data("spotifyId") && $("#end").data("spotifyId") != "" && $("#end").val() != "") {
      $("#end-field").addClass("input--filled");
    } else {
      $("#end").val("")
      $("#end-field").removeClass("input--filled");
    }
  })
});
