function TinyImagesFileBrowser(field_name, url, type, win) {

    var baseURL = tinyMCE.selectedInstance.settings['tiny_images_base_url'] || '/tinyimages/';
    var cmsURL = baseURL + type + "/";
    
    tinyMCE.selectedInstance.windowManager.open({
        url: cmsURL,
        width: 500,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no",
        field_name: field_name,
        win: win
    });
    return false;
}

function returnURL(url, alt, width, height) {
	var win = tinyMCEPopup.features['win']

	win.document.getElementById(tinyMCEPopup.features['field_name']).value = url;
	win.document.getElementById("alt").value = alt;
	win.document.getElementById("width").value = width;
	win.document.getElementById("height").value = height;
	tinyMCEPopup.close();
}
