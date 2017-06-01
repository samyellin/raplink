$(function() {
  $( "#start" ).autocomplete({
    source: function( request, response ) {
      var typeaheadUrl = 'http://127.0.0.1:5000/raplink/api/v1.0/typeahead?artist=' + encodeURI($("#start").val());
      $.ajax({
        url: typeaheadUrl,
        success: function( data ) {
          response( JSON.parse(data) );
        }
      });
    },
    minLength: 3,
    select: function( event, ui ) {
      console.log("Selected: " + ui.item.label);
    }
  });

  $( "#end" ).autocomplete({
    source: function( request, response ) {
      var typeaheadUrl = 'http://127.0.0.1:5000/raplink/api/v1.0/typeahead?artist=' + encodeURI($("#end").val());
      $.ajax({
        url: typeaheadUrl,
        success: function( data ) {
          response( JSON.parse(data) );
        }
      });
    },
    minLength: 3
  });
});