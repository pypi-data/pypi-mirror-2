tinyMCEPopup.requireLangPack();

var PlacegalleryDialog = {
	init : function() {
		var f = document.forms[0];

		// Get the selected contents as text and place it in the input
		f.someval.value = tinyMCEPopup.editor.selection.getContent({format : 'text'}) ;
		f.somearg.value = tinyMCEPopup.getWindowArg('some_custom_arg');
		
	},
	
	insert : function() {
		// Insert the contents from the input into the document
		myframe = '<iframe src="' + document.forms[0].someval.value + '/'  + document.forms[0].somearg.value +'"' + 'height="' + +document.forms[0].height.value +'"' + 'width="' + +document.forms[0].width.value +'"' + '>';
		tinyMCEPopup.editor.execCommand('mceInsertContent', true, myframe);
		tinyMCEPopup.close();
	}
};


tinyMCEPopup.onInit.add(PlacegalleryDialog.init, PlacegalleryDialog);
