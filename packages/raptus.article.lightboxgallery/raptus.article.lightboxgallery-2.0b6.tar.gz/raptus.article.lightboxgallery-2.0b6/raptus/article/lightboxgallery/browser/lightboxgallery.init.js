jQuery(document).ready(function() {
  var images = new Array();
  var settings = inlinelightbox.settings['raptus_article_lightboxgallery'];
  jQuery('a[rel^=lightboxgallery]').each(function() {
    var o = jQuery(this);
    var rel = o.attr('rel');
    if(jQuery.inArray(rel, images) == -1)
      images.push(rel);
  });
  for(var i=0; i<images.length; i++) {
    jQuery('a[rel="'+images[i]+'"]').inlineLightBox(settings);
  }
});
