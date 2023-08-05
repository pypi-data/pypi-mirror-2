var TinyMCE_FilePlugin = {
    getInfo : function() {
        return {
            longname : 'File Plugin',
            author : 'Yaco',
            authorurl : 'http://www.yaco.es',
            infourl : 'http://www.yaco.es',
            version : tinyMCE.majorVersion + "." + tinyMCE.minorVersion
        };
    },

	/**
	 * Returns the HTML contents of the preview control.
	 */
	getControlHTML : function(cn) {
		switch (cn) {
			case "file":
				return tinyMCE.getButtonHTML(cn, 'lang_file_desc', '{$pluginurl}/../images/file.gif', 'mceFile');
		}

		return "";
	},

	/**
	 * Executes the mceInternalLink command.
	 */
	execCommand : function(editor_id, element, command, user_interface, value) {
		// Handle commands
		switch (command) {
			case "mceFile":
				var fileURL = tinyMCE.getParam("plugin_file_url", null);
				var fileWidth = tinyMCE.getParam("plugin_file_url_width", "400");
				var fileHeight = tinyMCE.getParam("plugin_file_url_height", "350");

				// Use a custom preview page
				if (fileURL) {
					var template = new Array();

					template['file'] = fileURL;
					template['width'] = fileWidth;
					template['height'] = fileHeight;

					tinyMCE.openWindow(template, {editor_id : editor_id, resizable : "yes", scrollbars : "yes", inline : "yes", content : tinyMCE.getContent(), content_css : tinyMCE.getParam("content_css")});
				}

				return true;
		}

		return false;
	},
    handleNodeChange : function(editor_id, node, undo_index, undo_levels, visual_aid, any_selection) {
        if (node == null)
                return;

        do {
            if (node.nodeName == "A" && tinyMCE.getAttrib(node, 'href') != "") {
                    tinyMCE.switchClass(editor_id + '_file', 'mceButtonSelected');
                    return true;
            }
        } while ((node = node.parentNode));

        if (any_selection) {
                tinyMCE.switchClass(editor_id + '_file', 'mceButtonNormal');
                return true;
        }

        tinyMCE.switchClass(editor_id + '_file', 'mceButtonDisabled');

        return true;
    }


};

(function($) {
    $(document).ready(function () {
        tinyMCE.addPlugin('file', TinyMCE_FilePlugin);
        tinyMCE.setPluginBaseURL("file", "/media/tinyimages/js/");
	tinyMCE.addToLang('file',{
		desc : 'Insert file'
	});
    });
})(jQuery);
