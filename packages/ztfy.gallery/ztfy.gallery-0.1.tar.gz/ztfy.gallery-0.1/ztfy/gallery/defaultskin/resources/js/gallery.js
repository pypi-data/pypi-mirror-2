(function($) {

	$.ZBlog.gallery = {

		buy_image: function(id) {
			$('#fancybox-title').empty();
			$.get($('IMG[id='+id+']').parents('A').attr('href') + '/@@buy.html', function(data) {
				$('<span id="fancybox-title-over"></span>').addClass('nohide')
														   .append(data)
														   .appendTo($('#fancybox-title'));
			});
		},

		buy_image_from_thumbnail: function(id) {
			$.get($('IMG[id='+id+']').parents('A').attr('href') + '/@@buy.html', function(data) {
				$.fancybox('<div id="fancybox-title-over" class="fancybox-title-over">' + data + '</div>');
			});
		}

	}

	var lang = $('HTML').attr('lang') || $('HTML').attr('xml:lang');
	$.getScript('/++skin++ZBlog/@@/ztfy.blog.defaultskin.gallery.js/i18n/' + lang + '.js');

	if ($.fn.fancybox) {
		$(document).ready(function() {
			$('DIV.gallery IMG.thumbnail').parents('A').fancybox({
				type: 'image',
				overlayOpacity: 0.7,
				titleShow: true,
				titlePosition: 'over',
				titleFormat: function(title, array, index, opts) {
					var output = '';
					var has_title = title && title.length;
					if ($(array[0]).parents('DIV.gallery').attr('paypal_enabled') == 'True') {
						var id = $('IMG', $(array[index])).attr('id');
						if (id) {
							var klass = has_title ? '' : ' opaque';
							output = '<div class="caddie' + klass + '"><a href="javascript:$.ZBlog.gallery.buy_image(\'' + id + '\');">' +
									 '<img src="/++skin++ZBlog/@@/ztfy.blog.defaultskin.gallery.img/caddie.png" title="' + $.ZBlog.gallery.I18n.BUY_PICTURE + '" /></a></div>';
						}
					}
					if (has_title) {
						output += '<span id="fancybox-title-over"><strong>' + title + '</strong><br />' + $(array[index]).attr('description') + '</span>';
					}
					output += '<div class="clearer"><!-- IE bugfix --></div>';
					return output;
				},
				transitionIn: 'elastic',
				transitionOut: 'elastic',
				hideOnContentClick: true,
				onComplete: function() {
					$('<img></img>').attr('src', '/www.ids.com/++presentation++/++file++site_watermark')
									.css('position', 'absolute')
									.css('right', 30)
									.css('bottom', 30)
									.appendTo($('#fancybox-inner'));
					$("#fancybox-wrap").hover(function() {
						$("#fancybox-title").slideDown('slow');
					}, function() {
						if (!$('#fancybox-title-over').hasClass('nohide')) {
							$("#fancybox-title").slideUp('slow');
						}
					});
				}
			});
		});
	}

})(jQuery);