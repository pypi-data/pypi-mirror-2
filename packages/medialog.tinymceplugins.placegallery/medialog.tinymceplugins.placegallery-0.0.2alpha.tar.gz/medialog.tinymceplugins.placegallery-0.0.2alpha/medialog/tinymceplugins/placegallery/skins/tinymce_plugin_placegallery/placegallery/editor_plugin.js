/**
 * Plone gallery Plugin
 *
 * @author Espen Moe-Nilssen
 */

(function() {
    tinymce.create('tinymce.plugins.PlacegalleryPlugin', {
        init : function(ed, url) {
            // Register commands
            ed.addCommand('mcePlacegallery', function() {
                // Internal gallery object like a placeholder
                if (ed.dom.getAttrib(ed.selection.getNode(), 'class').indexOf('mceItem') != -1)
                    return;

                ed.windowManager.open({
                    file : url + '/dialog.htm',
                    width : 520 + parseInt(ed.getLang('placegallery.delta_width', 0)),
                    height : 300 + parseInt(ed.getLang('placegallery.delta_height', 0)),
                    inline : 1
                }, {
                    plugin_url : url, // Plugin absolute URL
					some_custom_arg : 'custom arg' // Custom argument
                });
            });

            // Register buttons
            ed.addButton('placegallery', {
                title : 'placegallery.desc',
                cmd : 'mcePlacegallery',
                image : url + '/img/placegallery.gif'
            });
            
            // Add a node change handler, selects the button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('placegallery', n.nodeName == 'IMG');
			})
        },
        
         /**
		 * Creates control instances based in the incomming name. This method is normally not
		 * needed since the addButton method of the tinymce.Editor class is a more easy way of adding buttons
		 * but you sometimes need to create more complex controls like listboxes, split buttons etc then this
		 * method can be used to create those.
		 *
		 * @param {String} n Name of the control to create.
		 * @param {tinymce.ControlManager} cm Control manager to use inorder to create new control.
		 * @return {tinymce.ui.Control} New control instance or null if no control was created.
		 */
		 
		 createControl : function(n, cm) {
			return null;
		},

		/**
		 * Returns information about the plugin as a name/value array.
		 * The current keys are longname, author, authorurl, infourl and version.
		 *
		 * @return {Object} Name/value array containing information about the plugin.
		 */

        getInfo : function() {
            return {
                longname : 'Placegallery Gallery Plugin',
                author : 'Placegallery Moe-Nilssen',
                authorurl : 'http://medialog.no',
                infourl : 'http://plone.org/products/tinymce',
                version : "0.1"
            };
        }
    });

    // Register plugin
    tinymce.PluginManager.add('placegallery', tinymce.plugins.PlacegalleryPlugin);
})();