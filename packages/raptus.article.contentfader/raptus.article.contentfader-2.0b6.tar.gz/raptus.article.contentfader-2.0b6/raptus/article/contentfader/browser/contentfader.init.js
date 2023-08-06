jQuery(document).ready(function() {
  var images = [];
  var settings = inlinelightbox.settings['raptus_article_contentfader'];
  jQuery('.contentfader.full li').inlineLightBox(settings);
  jQuery('.contentfader.full ul').hide();
  var settings = inlinelightbox.settings['raptus_article_contentfader_teaser'];
  jQuery('.contentfader.teaser li').inlineLightBox(settings);
  jQuery('.contentfader.teaser ul').hide();
});
