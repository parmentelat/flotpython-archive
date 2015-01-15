// leave at least 2 line with only a star on it below, or doc generation fails
/**
 *
 *
 * Placeholder for custom user javascript
 * mainly to be overridden in profile/static/custom/custom.js
 * This will always be an empty file in IPython
 *
 * User could add any javascript in the `profile/static/custom/custom.js` file
 * (and should create it if it does not exist).
 * It will be executed by the ipython notebook at load time.
 *
 * Same thing with `profile/static/custom/custom.css` to inject custom css into the notebook.
 *
 * Example :
 *
 * Create a custom button in toolbar that execute `%qtconsole` in kernel
 * and hence open a qtconsole attached to the same kernel as the current notebook
 *
 *    $([IPython.events]).on('app_initialized.NotebookApp', function(){
 *        IPython.toolbar.add_buttons_group([
 *            {
 *                 'label'   : 'run qtconsole',
 *                 'icon'    : 'icon-terminal', // select your icon from http://fortawesome.github.io/Font-Awesome/icons
 *                 'callback': function () {
 *                     IPython.notebook.kernel.execute('%qtconsole')
 *                 }
 *            }
 *            // add more button here if needed.
 *            ]);
 *    });
 *
 * Example :
 *
 *  Use `jQuery.getScript(url [, success(script, textStatus, jqXHR)] );`
 *  to load custom script into the notebook.
 *
 *    // to load the metadata ui extension example.
 *    $.getScript('/static/notebook/js/celltoolbarpresets/example.js');
 *    // or
 *    // to load the metadata ui extension to control slideshow mode / reveal js for nbconvert
 *    $.getScript('/static/notebook/js/celltoolbarpresets/slideshow.js');
 *
 *
 * @module IPython
 * @namespace IPython
 * @class customjs
 * @static
 */
// Wait until the notebook app has initialized
$([IPython.events]).on('app_initialized.NotebookApp', function(){
  
    // Add a shortcut
    // the 'help' text will show up in the help page (CTRL-M h or ESC h)
    // the 'handler' code is executed whenever this shortcut is used
    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-x', {
	help: 'Clear all output',                  
	handler: function (event) {                
	    IPython.notebook.clear_all_output();   
	    return false;                          
	}
    });

    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-0', {
	help: 'Restart kernel - no question asked',
	handler: function (event) {
	    IPython.notebook.kernel.restart();
	    return false;
	}
    });

    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-a', {
	help: 'Run all cells',
	handler: function (event) {
	    IPython.notebook.execute_all_cells();
	    return false;
	}
    });

    // all 3 steps in one keystroke
    // this won't work too well; the first 2 steps work fine but then
    // it clearly feels like we should wait for the kernel to come up
    // for now it does the 2 first steps just fine though
    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-f', {
	help: 'Fullmonty: check notebook from scratch',
	handler: function (event) {
	    IPython.notebook.clear_all_output();   
	    IPython.notebook.kernel.restart();
	    IPython.notebook.execute_all_cells();
	    return false;
	}
    });

    // also support ctrl-m ctrl-s in addition to ctrl-m s
    IPython.keyboard_manager.command_shortcuts.add_shortcut('ctrl-s', {
	help: 'Run all cells',
	handler: function (event) {
	    IPython.notebook.save_notebook();
	    return false;
	}
    });
    
  // A small hint so we can see through firebug that our custom code executed
  console.log("Custom shortcut(s) loaded");
});
