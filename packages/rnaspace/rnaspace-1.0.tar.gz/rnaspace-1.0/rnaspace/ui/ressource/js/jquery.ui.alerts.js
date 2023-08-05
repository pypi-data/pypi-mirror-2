// jQuery Alert Dialogs Plugin
//
// Version 1.0
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
// 29 December 2008
//
// Visit http://abeautifulsite.net/notebook/87 for more information
//
// Usage:
//		jAlert( message, [title, callback] )
//		jConfirm( message, [title, callback] )
//		jPrompt( message, [value, title, callback] )
//
// History:
//
//		1.00 - Released (29 December 2008)
//
// License:
//
//		This plugin is licensed under the GNU General Public License: http://www.gnu.org/licenses/gpl.html
//
(function($) {

	$.alerts = {

		// These properties can be read/written by accessing $.alerts.propertyName from your scripts at any time
		overlayOpacity: 0.5,                // transparency level of overlay
		overlayColor: '#000',               // base color of overlay
		okButton: '&nbsp;OK&nbsp;',         // text for the OK button
		cancelButton: '&nbsp;Cancel&nbsp;', // text for the Cancel button

		// Public methods
		alert: function(message, title, callback) {
			if( title == null ) title = 'Alert';
			$.alerts._show(title, message, null, 'alert', function(result) {
				if( callback ) callback(result);
			});
		},
		confirm: function(message, title, callback) {
			if( title == null ) title = 'Confirm';
			$.alerts._show(title, message, null, 'confirm', function(result) {
				if( callback ) callback(result);
			});
		},
		prompt: function(message, value, title, callback) {
			if( title == null ) title = 'Prompt';
			$.alerts._show(title, message, value, 'prompt', function(result) {
				if( callback ) callback(result);
			});
		},

		// Private methods
		_show: function(title, msg, value, type, callback) {
			$.alerts._hide();
			$("BODY").append('<div id="popup_dialog" title=""></div>');
			$("#popup_dialog").dialog({
			    autoOpen: false,
		        width: 250,
		        minHeight: 80,
		        bgiframe: true,
		        resizable: false,
		        position: 'center',
			    modal: true,
		        overlay: {
		            backgroundColor: $.alerts.overlayColor,
		            opacity: $.alerts.overlayOpacity
		        }
		    });
		    $("#popup_dialog").dialog('option', 'title', title);
		    $("#popup_dialog").html('<div class="cbb_content">' + msg + '</div>')
			switch( type ) {
				case 'alert':
					$("#popup_dialog").after('<div style="float:right;"> <input type="button" class="button_bp" value="' + $.alerts.okButton + '" id="popup_ok" /></div>');
					$("#popup_ok").click( function() {
						$.alerts._hide();
						callback(true);
					});
					$("#popup_ok").focus().keypress( function(e) {
						if( e.keyCode == 13 || e.keyCode == 27 ) $("#popup_ok").trigger('click');
					});
				break;
				case 'confirm':
					$("#popup_dialog").after('<div style="float:right;"><input type="button" class="button_bp" value="' + $.alerts.okButton + '" id="popup_ok" /> <input type="button" class="button_bp" value="' + $.alerts.cancelButton + '" id="popup_cancel" /></div>');
					$("#popup_ok").click( function() {
						$.alerts._hide();
						if( callback ) callback(true);
					});
					$("#popup_cancel").click( function() {
						$.alerts._hide();
						if( callback ) callback(false);
					});
					$("#popup_ok").focus();
					$("#popup_ok, #popup_cancel").keypress( function(e) {
						if( e.keyCode == 13 ) $("#popup_ok").trigger('click');
						if( e.keyCode == 27 ) $("#popup_cancel").trigger('click');
					});
				break;
				case 'prompt':
					$("#popup_dialog").append('<br /><input type="text" class="customizeinput" size="30" id="popup_prompt" />').after('<div style="float:right;><input type="button" class="button_bp" value="' + $.alerts.okButton + '" id="popup_ok" /> <input type="button" value="' + $.alerts.cancelButton + '" id="popup_cancel" /></div>');
					$("#popup_ok").click( function() {
						var val = $("#popup_prompt").val();
						$.alerts._hide();
						if( callback ) callback( val );
					});
					$("#popup_cancel").click( function() {
						$.alerts._hide();
						if( callback ) callback( null );
					});
					$("#popup_prompt, #popup_ok, #popup_cancel").keypress( function(e) {
						if( e.keyCode == 13 ) $("#popup_ok").trigger('click');
						if( e.keyCode == 27 ) $("#popup_cancel").trigger('click');
					});
					if( value ) $("#popup_prompt").val(value);
					$("#popup_prompt").focus().select();
				break;
			}
			$("#popup_dialog").dialog("open");
		},
		_hide: function() {
			$("#popup_dialog").dialog("close");
			$("#popup_dialog").remove();
		}
	}

	// Shortuct functions
	jAlert = function(message, title, callback) {
		$.alerts.alert(message, title, callback);
	}
	jConfirm = function(message, title, callback) {
		$.alerts.confirm(message, title, callback);
	};
	jPrompt = function(message, value, title, callback) {
		$.alerts.prompt(message, value, title, callback);
	};
})(jQuery);