var onMouseOutOpacity = 0.67;

$('.gallery-thumbs ul.thumbs li').css('opacity', onMouseOutOpacity).hover(
  function () {
  $(this).not('.selected').fadeTo('fast', 1.0);
}, 
  function () {
    $(this).not('.selected').fadeTo('fast', onMouseOutOpacity);
});

$(document).ready(function() {
    var gallery = $('.gallery').galleriffic('.gallery-thumbs', {
        delay:                  3000,
        numThumbs:              20,
        preloadAhead:           40, // Set to -1 to preload all images
        enableTopPager:         false,
        enableBottomPager:      true,
        imageContainerSel:      '.main-image',
        controlsContainerSel:   '.controls',
        captionContainerSel:    '.captions',
        loadingContainerSel:    '.loader',
        renderSSControls:       true,
        renderNavControls:      true,
        playLinkText:           'Play',
        pauseLinkText:          'Pause',
        prevLinkText:           'Previous',
        nextLinkText:           'Next',
        nextPageLinkText:       'Next &rsaquo;',
        prevPageLinkText:       '&lsaquo; Prev',
        enableHistory:          true,
        autoStart:              false,
        onChange:              function(prevIndex, nextIndex) {
	  $('.gallery-thumbs ul.thumbs').children()
	  .eq(prevIndex).fadeTo('fast', onMouseOutOpacity).end()
	  .eq(nextIndex).fadeTo('fast', 1.0);
	},
	onTransitionOut:        function(callback) {
	  $('.main-image, #caption').fadeOut(callback);
	},
	onTransitionIn:         function() {
	  $('.main-image, #caption').fadeIn();
	},
	onPageTransitionOut:    function(callback) {
	  $('.gallery-thumbs ul.thumbs').fadeOut(callback);
	},
	onPageTransitionIn:     function() {
	  $('.gallery-thumbs ul.thumbs').fadeIn();
	}
    });
});
