(function($) {
  $(document).ready(function() {
    if($('#portal-content-headerfader li a').size() > 1) {
      $('#portal-content-headerfader li a').inlineLightBox(inlinelightbox.settings['raptus_headerfader']);
      $('#portal-content-headerfader > ul').hide();
    }
  });
})(jQuery);