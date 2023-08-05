var callThemeroller = function(hash) {
    // thats not working like expected: so its disabled

    // give the current hash to the themeroller, so he can take the settings of the theme
    // if (hash) {
    //  window.location.href += '#'+hash;
    // }

    if (!/Firefox[\/\s](\d+\.\d+)/.test(navigator.userAgent)) {
        alert('Sorry, due to security restrictions, this tool only works in Firefox');
        return false;
    };
    if (window.jquitr) {
        jquitr.addThemeRoller();
    } else {
        jquitr = {};
        jquitr.s = document.createElement('script');
        jquitr.s.src = 'http://jqueryui.com/themeroller/developertool/developertool.js.php';
        document.getElementsByTagName('head')[0].appendChild(jquitr.s);
    }
    $('#ploneDownloadTheme').show();
};

var ploneDownloadTheme = function() {
    var hash = jquitr.getHash();
    var name = $('#themename input').val();
    if (!hash) {
        alert("Nothing themed - please use themeroller");
    }
    if (!name || (name.match(/[a-z]*/) != name)) {
        alert("You must enter a name containing only a-z characters");
    } else {
        document.location.href = 'portal_ui_tool/download?name='+name+'&hash='+encodeURIComponent(hash);
    }
};

var createDLDirectory = function() {
    document.location.href = 'portal_ui_tool/createDLDirectory';
};
