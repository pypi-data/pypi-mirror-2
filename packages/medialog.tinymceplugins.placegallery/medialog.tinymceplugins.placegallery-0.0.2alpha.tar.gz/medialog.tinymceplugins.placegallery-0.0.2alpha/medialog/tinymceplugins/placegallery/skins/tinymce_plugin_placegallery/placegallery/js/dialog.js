tinyMCEPopup.requireLangPack();

var PlacegalleryDialog = {
	init : function() {
		var f = document.forms[0];

		// Get the selected contents as text and place it in the input
		f.somelink.value = tinyMCEPopup.editor.selection.getContent({format : 'text'}) ;
		f.someview.value = tinyMCEPopup.getWindowArg('some_custom_arg');
		
	},
	
	insert : function() {
		// Insert the contents from the input into the document
		myframe = '<iframe src="' + document.forms[0].somelink.value + '/'  + document.forms[0].someview.value + '"' + 'height="' + document.forms[0].height.value + '"' + 'width="' + document.forms[0].width.value + '"' + 'overflow="' +
		document.forms[0].overflow.value + '"' + 'background="' + document.forms[0].background.value + '"></iframe>';
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, myframe);
		tinyMCEPopup.close();
	}
};


tinyMCEPopup.onInit.add(PlacegalleryDialog.init, PlacegalleryDialog);
