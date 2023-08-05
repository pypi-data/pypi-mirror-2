/**
 * ZTFY.file cthumb management
 */

(function($) {

	if (!$.ztfy) {
		$.ztfy = {}
	}

	$.ztfy.file = {

		cthumb: {
			endDrag: function(event) {
				var $input = $('INPUT[type="file"]', $(this).parents('DIV.cthumb-widget'));
				var $form = $input.parents('FORM');
				var name = $input.attr('name');
				// Try to handle I18n widgets
				var lio_list = name.lastIndexOf(':list');
				if (lio_list != -1) {
					var id = $input.attr('id');
					var lio_lang = id.lastIndexOf('-');
					if (lio_lang != -1) {
						var lang = id.substr(lio_lang+1);
						name = name.substr(0,lio_list) + '_' + lang;
					}
				}
				var position = $(this).position();
				$('INPUT[name="' + name + '__x"]').val(position.left);
				$('INPUT[name="' + name + '__y"]').val(position.top);
			},

			endResize: function(event) {
				var $input = $('INPUT[type="file"]', $(this).parents('DIV.cthumb-widget'));
				var $form = $input.parents('FORM');
				var name = $input.attr('name');
				// Try to handle I18n widgets
				var lio_list = name.lastIndexOf(':list');
				if (lio_list != -1) {
					var id = $input.attr('id');
					var lio_lang = id.lastIndexOf('-');
					if (lio_lang != -1) {
						var lang = id.substr(lio_lang+1);
						name = name.substr(0,lio_list) + '_' + lang;
					}
				}
				var position = $(this).position();
				$('INPUT[name="' + name + '__w"]').val($(this).width());
				$('INPUT[name="' + name + '__h"]').val($(this).height());
			}
		}   // $.ztfy.file.cthumb

	};  // $.ztfy.file

	$(document).ready(function() {
		$('DIV.cthumb').each(function() {
			var $img = $('IMG.thumb', $(this).parent());
			$(this).draggable({ containment: $img,
								stop: $.ztfy.file.cthumb.endDrag });
			$(this).resizable({ containment: $img,
								aspectRatio: true,
								autoHide: true,
								minWidth: 20,
								minHeight: 20,
								stop: $.ztfy.file.cthumb.endResize });
		});
	});

})(jQuery);
