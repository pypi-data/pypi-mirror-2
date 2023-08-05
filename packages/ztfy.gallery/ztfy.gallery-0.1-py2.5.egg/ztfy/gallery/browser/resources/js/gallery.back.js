(function($) {

	$.ZBlog.gallery = {

		sort_options: {
			handle: 'DIV.image',
			containment: 'parent',
			placeholder: 'sorting-holder',
			stop: function(event, ui) {
				var ids = new Array();
				$('FIELDSET.gallery DIV.image').each(function (i) {
					ids[ids.length] = $(this).attr('id');
				});
				var data = {
					ids: ids
				}
				$.ZBlog.ajax.post(window.location.href + '/@@ajax/ajaxUpdateOrder', data, null, function(request, status, error) {
					jAlert(request.responseText, $.ZBlog.I18n.ERROR_OCCURED, window.location.reload);
				});
			}
		},

		remove: function(oid, source) {
			jConfirm($.ZBlog.I18n.CONFIRM_REMOVE, $.ZBlog.I18n.CONFIRM, function(confirmed) {
				if (confirmed) {
					var data = {
						id: oid
					}
					$.ZBlog.form.ajax_source = $('DIV[id='+source+']');
					$.ZBlog.ajax.post(window.location.href + '/@@ajax/ajaxRemove', data, $.ZBlog.gallery._removeCallback, null, 'text');
				}
			});
		},

		_removeCallback: function(result, status) {
			if ((status == 'success') && (result == 'OK')) {
				$($.ZBlog.form.ajax_source).parents('DIV.image_wrapper').remove();
			}
		}

	}

})(jQuery);