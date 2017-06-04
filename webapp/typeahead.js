$(function() {

  typeaheadResultHandler = function(ul, item) {
    var connectedIcon;
    if (item.connected) {
      connectedIcon = '<i class="fa fa-check-square" aria-hidden="true"></i>'
    } else {
      connectedIcon = '<i class="fa fa-window-close" aria-hidden="true"></i>'
    }
    return $( "<li>" )
      .append( "<div>" + item.name + " " + connectedIcon + "</div>")
      .appendTo( ul );
  }

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
      $( "#start" ).data("spotifyId", ui.item.spotifyId)
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
      $( "#end" ).data("spotifyId", ui.item.spotifyId)
      return false;
    },
    minLength: 1
  })
  .autocomplete( "instance" )._renderItem = typeaheadResultHandler;
});
