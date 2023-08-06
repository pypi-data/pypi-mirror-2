$(document).ready(function() {

    var onMouseOutOpacity = 0.67;

    $('.gallery-thumbs ul.thumbs li').css('opacity', onMouseOutOpacity).hover(
	function () {
	    $(this).not('.selected').fadeTo('fast', 1.0);
	}, 
	function () {
	    $(this).not('.selected').fadeTo('fast', onMouseOutOpacity);
    });

    // Initialize Advanced Galleriffic Gallery
    var gallery = $('.gallery-thumbs').galleriffic({
	delay:                     2500,
	numThumbs:                 15,
	preloadAhead:              10,
	enableTopPager:            true,
	enableBottomPager:         true,
	maxPagesToShow:            7,
	imageContainerSel:         '.gallery .slideshow',
	controlsContainerSel:      '.gallery .controls',
	captionContainerSel:       '.gallery .caption',
	loadingContainerSel:       '.gallery .loader',
	renderSSControls:          true,
	renderNavControls:         true,
	playLinkText:              'Play',
	pauseLinkText:             'Pause',
	prevLinkText:              '&lsaquo; Previous',
	nextLinkText:              'Next &rsaquo;',
	nextPageLinkText:          'Next &rsaquo;',
	prevPageLinkText:          '&lsaquo; Prev',
	enableHistory:             false,
	autoStart:                 false,
	syncTransitions:           false,
	defaultTransitionDuration: 900,
	onSlideChange:             function(prevIndex, nextIndex) {
	    this.find('ul.thumbs').children()
		.eq(prevIndex).fadeTo('fast', onMouseOutOpacity).end()
		.eq(nextIndex).fadeTo('fast', 1.0);
	},
	onPageTransitionOut:       function(callback) {
	    this.fadeTo('fast', 0.0, callback);
	},
	onPageTransitionIn:        function() {
	    this.fadeTo('fast', 1.0);
	}
    });
});
