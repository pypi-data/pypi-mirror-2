jQuery(document).ready(function() {
  function getLatLng() {
    jQuery('#spinner').show();
    geocoder = new GClientGeocoder();
    geocoder.getLatLng(jQuery('#geocode').val(), function(center) {
      if(center) {
        jQuery('#longitude').val(center.x);
        jQuery('#latitude').val(center.y);
      }
      jQuery('#spinner').hide();
    });
  }
  if(jQuery('#archetypes-fieldname-geocode').length) {
    jQuery('#archetypes-fieldname-geocode').append('<input type="hidden" name="longitude" id="longitude" /><input type="hidden" name="latitude" id="latitude" />');
    jQuery('#archetypes-fieldname-longitude, #archetypes-fieldname-latitude').remove();
    jQuery('#archetypes-fieldname-geocode').show();
    jQuery('#geocode').blur(getLatLng);
    getLatLng();
  }
});
