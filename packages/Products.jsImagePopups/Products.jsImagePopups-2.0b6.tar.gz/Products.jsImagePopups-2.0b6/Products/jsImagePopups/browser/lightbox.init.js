jQuery(document).ready(function() {
  var images = [];
  jQuery('a[rel^=lightbox]').each(function() {
    var o = jQuery(this);
    var rel = o.attr('rel');
    if((rel.length == 8 || rel.indexOf('lightbox[') === 0) && jQuery.inArray(rel, images) == -1)
      images.push(rel);
  });
  for(var i=0; i<images.length; i++)
    jQuery('a[rel="'+images[i]+'"]').lightBox(lightbox_settings);
  
  jQuery('a[href*=image_view_fullscreen]').each(function() {
    var o = jQuery(this);
    o.attr('href', o.attr('href').replace('image_view_fullscreen', 'image_preview'));
    o.lightBox(lightbox_settings);
  });
  
  jQuery('.photoAlbumEntry a').each(function() {
    var o = jQuery(this);
    o.attr('href', o.attr('href').replace('view', 'image_preview'));
  });
  jQuery('.photoAlbumEntry a').lightBox(lightbox_settings);
});
