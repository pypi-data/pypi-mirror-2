var url = tinyMCE.getParam("external_image_list_url");
if (url != null) {
	// Fix relative
	if (url.charAt(0) != '/' && url.indexOf('://') == -1)
		url = tinyMCE.documentBasePath + "/" + url;

	document.write('<sc'+'ript language="javascript" type="text/javascript" src="' + url + '"></sc'+'ript>');
}

function insertImage() {
	var src = document.forms[0].src.value;
	
	tinyMCEPopup.restoreSelection();
	tinyMCE.themes['advanced']._insertLink(src);
	tinyMCEPopup.close();
}

    function init() {
	tinyMCEPopup.resizeToInnerSize();

	document.getElementById('srcbrowsercontainer').innerHTML = getBrowserHTML('srcbrowser','src','file','theme_advanced_image');

	var formObj = document.forms[0];


	formObj.src.value = tinyMCE.getWindowArg('src') || "";
	formObj.insert.value = tinyMCE.getLang('lang_' + tinyMCE.getWindowArg('action'), 'Insert', true); 

	// Handle file browser
	if (isVisible('srcbrowser'))
		document.getElementById('src').style.width = '180px';

	// Auto select image in list
	if (typeof(tinyMCEImageList) != "undefined" && tinyMCEImageList.length > 0) {
		for (var i=0; i<formObj.image_list.length; i++) {
			if (formObj.image_list.options[i].value == tinyMCE.getWindowArg('src'))
				formObj.image_list.options[i].selected = true;
		}
	}
}

var preloadImg = new Image();

function resetImageData() {
	var formObj = document.forms[0];
	formObj.width.value = formObj.height.value = "";	
}

function updateImageData() {
	var formObj = document.forms[0];

	if (formObj.width.value == "")
		formObj.width.value = preloadImg.width;

	if (formObj.height.value == "")
		formObj.height.value = preloadImg.height;
}

function getImageData() {
	preloadImg = new Image();
	tinyMCE.addEvent(preloadImg, "load", updateImageData);
	tinyMCE.addEvent(preloadImg, "error", function () {var formObj = document.forms[0];formObj.width.value = formObj.height.value = "";});
	preloadImg.src = tinyMCE.convertRelativeToAbsoluteURL(tinyMCE.settings['base_href'], document.forms[0].src.value);
}


function getBrowserHTML(id, target_form_element, type, prefix) {
    var option = prefix + "_" + type + "_browser_callback";
    var cb = tinyMCE.getParam(option, tinyMCE.getParam("file_browser_callback"));
    if (cb == null)
        return "";

    var html = "";

    html += '<a id="' + id + '_link" href="javascript:openBrower(\'' + id + '\',\'' + target_form_element + '\', \'' + type + '\',\'' + option + '\');" onmousedown="return false;">';
    html += '<img id="' + id + '" src="/media/tinyimages/js/images/browse.gif"';
    html += ' onmouseover="this.className=\'mceButtonOver\';"';
    html += ' onmouseout="this.className=\'mceButtonNormal\';"';
    html += ' onmousedown="this.className=\'mceButtonDown\';"';
    html += ' width="20" height="18" border="0" title="' + tinyMCE.getLang('lang_browse') + '"';
    html += ' class="mceButtonNormal" alt="' + tinyMCE.getLang('lang_browse') + '" /></a>';

    return html;
}

