(function($) {

	if (typeof($.ZBlog) == 'undefined') {
		$.ZBlog = {};
	}

	var loading = null;
	var loadingFrame = 1;
	var loadingTimer = null;
	var background_url = null;

	$.ZBlog.gallery.skin = {

		animateLoading: function() {
			if (!loading.is(':visible')){
				clearInterval(loadingTimer);
				return;
			}
			loading.css('background-position-y', (loadingFrame * -40) + 'px');
			loadingFrame = (loadingFrame + 1) % 12;
		},

		loadBackground: function() {
			loading = $('#banner DIV');
			loadingTimer = setInterval(this.animateLoading, 66);
			$.getJSON('getBackgroundURL.json', function(data) {
				if (data != 'none') {
					$.get(data.url, function(img) {
						$('#banner').css('background', 'transparent url('+data.url+') scroll no-repeat left top');
						$('#legend SPAN').text(data.title);
						loading.hide();
					});
				} else {
					loading.hide();
				}
			});
		}
	}

	/**
	 * Disable options menu !!
	 */
	$(document).bind('contextmenu', function() {
		return false;
	});

})(jQuery);