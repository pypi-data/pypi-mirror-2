// little helper to get width of hidden elements
jQuery.fn.evenIfHidden = function( callback ) {
    return this.each( function() {
	var self = $(this);
	var styleBackups = [];
	
	var hiddenElements = self.parents().andSelf().filter(':hidden');
	
	if ( ! hiddenElements.length ) {
	    callback( self );
	    return true; //continue the loop
	}
	
	hiddenElements.each( function() {
	    var style = $(this).attr('style');
	    style = typeof style == 'undefined'? '': style;
	    styleBackups.push( style );
	    $(this).attr( 'style', style + ' display: block !important;' );
	});
	
	hiddenElements.eq(0).css( 'left', -10000 );
	
	callback(self);
	
	hiddenElements.each( function() {
	    $(this).attr( 'style', styleBackups.shift() );
	});
    });
};

var rulesToRemove = {};

// this builds a data structure of all rules to remove
// its called by every "part" which must remove some of the
// default css rules of plone.
var removeRule = function(selector, styleCSS, styleJS) {
    if (!document.styleSheets[0]['cssRules']) { // IE don't like combined rules - they must be splitted
        if (selector.indexOf(', ') != -1) {
            var parts = selector.split(', ');
            for (var p=0; p<parts.length; p++) {
                removeRule(parts[p], styleCSS, styleJS);
            }
        }
    }
    if (rulesToRemove[selector]) {
        rulesToRemove[selector].push([styleCSS, styleJS]);
    } else {
        rulesToRemove[selector] = [[styleCSS, styleJS]];
    }
};

// this uses the populated rulesToRemove list to remove
// (hopefully efficentally) the rules from the style objects
var removeRules = function() {
    if (document.styleSheets[0]['cssRules']) { // FF/Dom Variant
        for(var i=0; i<document.styleSheets.length; i++) {
            var sheet = document.styleSheets[i];
            if (sheet.href && sheet.href.indexOf('/css') == -1 && sheet.cssRules.length) {
		if (sheet.cssRules[0].cssRules) {
                    for (var j=0; j<sheet.cssRules[0].cssRules.length; j++) {
			for (var selector in rulesToRemove) {
                            if (sheet.cssRules[0].cssRules[j].selectorText == selector) {
				// we found the selector - now look at the style setting
				for (var s=0; s<rulesToRemove[selector].length; s++) {
                                    var rule = sheet.cssRules[0].cssRules[j];
                                    var styleCSS = rulesToRemove[selector][s][0];
                                    var styleJS = rulesToRemove[selector][s][1];
                                    for (var k=0; k<rule.style.length; k++) {
					if (rule.style[k] == styleCSS) {
                                            rule.style[styleJS] = null;
					}
                                    }
				}
                            }
			}
		    }
                }
            }
        }
    }
    else { // IE variant
	for(var i=0; i<document.styleSheets.length; i++) {
            var sheet = document.styleSheets[i];
            if (sheet.href && sheet.href.indexOf('/css') == -1 && sheet.rules.length) {
                for (var j=0; j<sheet.rules.length; j++) {
                    for (var selector in rulesToRemove) {
                        if (sheet.rules[j].selectorText.toLowerCase() == selector.toLowerCase()) {
                            for (var s=0; s<rulesToRemove[selector].length; s++) {
                                var styleJS = rulesToRemove[selector][s][1];
				try {
                                    sheet.rules[j].style[styleJS] = '';
				} catch(e) { null }; // somes are added for chrome and causing problems here
                            }
                        }
                    }
                }
            }
        }
    }
};

var enableFonts = function() {
    $('body').addClass('ui-widget');
    removeRule('h1, h2, h3, h4, h5, h6', 'font-family', 'fontFamily');
    removeRule('#content .documentDescription, #content #description', 'font', 'font'); // needed for chrome
    removeRule('#content .documentDescription, #content #description', 'font-family', 'fontFamily');
}

var enablePersonalTool = function() {
    removeRule('#portal-personaltools', 'background-color', 'backgroundColor');
    removeRule('#portal-personaltools', 'background-position', 'backgroundPosition');
    removeRule('#portal-personaltools', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-personaltools', 'background-image', 'backgroundImage');
    removeRule('#portal-personaltools dt.actionMenuHeader a:focus, #portal-personaltools dt.actionMenuHeader a:hover', 'color', 'color');
    removeRule('#portal-personaltools', '-moz-border-radius-bottomleft', 'MozBorderRadiusBottomleft');
    removeRule('#portal-personaltools', '-moz-border-radius-bottomright', 'MozBorderRadiusBottomright');

    $('#portal-personaltools').addClass('ui-helper-reset ui-state-default ui-corner-bottom').hover(function() {
        $(this).addClass('ui-state-hover');
    }, function() {
        $(this).removeClass('ui-state-hover');
    });

    removeRule('#portal-personaltools dd', 'background-color', 'backgroundColor');
    removeRule('#portal-personaltools dd', 'background-position', 'backgroundPosition');
    removeRule('#portal-personaltools dd', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-personaltools dd', 'background-image', 'backgroundImage');
    removeRule('#portal-personaltools dd a:hover', 'background-color', 'backgroundColor');
    removeRule('#portal-personaltools dd a:hover', 'background-position', 'backgroundPosition');
    removeRule('#portal-personaltools dd a:hover', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-personaltools dd a:hover', 'background-image', 'backgroundImage');
    removeRule('#portal-personaltools dd a:hover', 'color', 'color');
    $('#portal-personaltools dd').addClass('ui-helper-reset ui-state-default ui-corner-all').css('top', '22px');

    $('#portal-personaltools dd a').hover(function() {
        $(this).addClass('ui-state-hover');
    }, function() {
        $(this).removeClass('ui-state-hover');
    });
};

var enableStatusMessage = function() {
    var $status = $('dl.portalMessage.info,dl.portalMessage.warning,dl.portalMessage.error');
    $status.each(function() {
		     if ($(this).attr('id') != 'kssPortalMessage') {
			 $(this).hide(); // hide the plone message
			 var label = $(this).find('dt').html();
			 var content = $(this).find('dd').html();
			 if ($(this).hasClass('error')) {
			     var template = '<div class="ui-custom-status-container ui-state-error ui-corner-all"><p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-alert"></span><strong>'+label+'</strong>\n'+content+'</p></div>';
			 } else {
			     var template = '<div class="ui-custom-status-container ui-state-highlight ui-corner-all"><p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-info"></span><strong>'+label+'</strong>\n'+content+'</p></div>';
			 }
			 $('#viewlet-above-content').after(template);
		     }
		 });
};

var forms_are_enabled = false; // gets set via tool.js()
var enableForms = function($content) {
    if (!$content) {
	var $content = $('body');
    }

    $content.find('.optionsToggle').removeClass('optionsToggle');
    $content.find('input,select,textarea').addClass('ui-widget-content ui-corner-all ui-button-text hover');
    $content.find('input,select,textarea').wrap('<span class="ui-button-text-only"></span>').css({'padding-left': '4px', 'padding-right': '4px'});
    
    $content.find('select, textarea, input:text, input:password').bind({
	focusin: function() {
            $(this).addClass('ui-state-focus');
        },
        focusout: function() {
            $(this).removeClass('ui-state-focus');
        }
    });

    $content.find('input:checkbox').each(function() {
    	var $label = $('<label />').insertBefore($(this));
        $(this).hide();
        $label.css({width:16,height:16,display:"inline-block"});
        $label.wrap('<span class="ui-widget-content ui-corner-all" style="display:inline-block;width:16px;height:16px;margin-right:5px;"/>');
        $label.parent().addClass('hover');
        $label.parent("span").click(function(event) {
            $(this).toggleClass("ui-state-active");
            $label.toggleClass("ui-icon ui-icon-check");
            $(this).next().click(); // trigger click on checkbox
    	});
	// initialize already checked ones
	if ($(this).attr('checked')) {
	    $label.parent("span").toggleClass("ui-state-active");
	    $label.toggleClass("ui-icon ui-icon-check");
	}

    });

    $content.find('input:radio').each(function() {
	var $label = $('<label />').insertBefore($(this));
	$(this).hide();
	$label.addClass("ui-icon ui-icon-radio-off");
	$label.wrap('<span class="ui-widget-content ui-corner-all" style="display:inline-block;width:16px;height:16px;margin-right:5px;"/>');
	$label.parent().addClass('hover');
	$label.parent("span").click(function(event) {
	    if ($(this).next().attr('checked')) {
		return // do nothing, if radiobox is already checked
	    }
	    // disable other radios of this group
	    var checkbox_name = $(this).parent().find('input:radio').attr('name');
	    var checkbox_value = $(this).parent().find('input:radio').val(); 
	    $content.find('input:radio[name='+checkbox_name+']').each(function() {
		if ($(this).val() != checkbox_value && $(this).attr('checked')) {
		    $(this).parent().find('label').parent('span').toggleClass("ui-state-active");
		    $(this).parent().find('label').toggleClass("ui-icon-radio-off ui-icon-bullet");
		    $(this).next().click();
		}
	    });
	    // check this radio
	    $(this).toggleClass("ui-state-active");
	    $label.toggleClass("ui-icon-radio-off ui-icon-bullet");
	    $(this).next().click();
	});
	// initialize already checked ones
	if ($(this).attr('checked')) {
	    $label.parent("span").toggleClass("ui-state-active");
	    $label.toggleClass("ui-icon-radio-off ui-icon-bullet");
	}
    });

    $content.find(".hover").hover(function(){
        $(this).addClass("ui-state-hover");
    },function(){
        $(this).removeClass("ui-state-hover");
    });

    // buttons
    $("input:submit").button();
    $("button").button();

    // and livesearch
    removeRule('input.inputLabelActive', 'color', 'color');
    removeRule('#livesearchLegend', 'background-color', 'backgroundColor');
    
    $('#LSResult').css('z-index', '100');
    $('#LSShadow').addClass('ui-corner-all ui-state-focus');
}

var enableDialogs = function() {
    $("a.link-overlay").unbind('click').click(function() {
        // remove old dialogs
        $('#dialogContainer').remove();

        // use the links content as default title of the dialog
        var title = $(this).html();
        $.get($(this).attr('href'),
              {},
	      function(data) {
		  showDialogContent(data,title)
	      }
	     );
        return false; // avoid the execution of the regular link
    });
};

var showDialogContent = function(data, title) {
    var $content = $(data).find('#content');

    // take the first heading as dialog title, if available
    $content.find('h1.documentFirstHeading').each(function() {
        title = $(this).html();
        $(this).hide();
    });
    $('<div id="dialogContainer" title="'+title+'"></div>').appendTo('body');
    
    // search for submit buttons and use them as dialog buttons
    var buttons = {};
    $content.find('input[type=submit]').each(function() {
        var buttonValue = $(this).val();
        buttons[buttonValue] = function() {
            $('input[type=submit][value='+buttonValue+']').click();
        };
        $(this).hide();
    });
    
    // bring up the dialog
    $content.appendTo('#dialogContainer');
    if (forms_are_enabled) {
	enableForms($content);
    }
    var $dialog = $('#dialogContainer').dialog({width: '60%', buttons: buttons});
};

var enableTabs = function() {
    removeRule('#content a:visited, dl.portlet a:visited', 'color', 'color');
    removeRule('#content a:link, dl.portlet a:link', 'color', 'color');
    removeRule('#content a:hover, dl.portlet a:hover', 'color', 'color');
    removeRule('#content a:focus, #content a:hover, dl.portlet a:focus, dl.portlet a:hover', 'color', 'color');

    $('<div class="ui-tabs ui-widget ui-widget-content ui-corner-all"></div>').insertBefore($('ul.formTabs'));
    $('ul.formTabs').appendTo('div.ui-tabs');
    $('fieldset').appendTo('div.ui-tabs');
    $('ul.formTabs').addClass('ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-top').removeClass('formTabs');
    $('div.ui-tabs ul li.formTab').addClass('ui-state-default ui-corner-top').removeClass('formTab').css('display', 'inline').hover(function() {
        $(this).addClass('ui-state-hover');
    }, function() {
        $(this).removeClass('ui-state-hover');
    });
    $('div.ui-tabs li a').click(function() {
        $(this).parent().parent().find('.ui-state-active').removeClass('ui-state-active');
        $(this).parent().addClass('ui-state-active');
    });
    $('ul.ui-tabs-nav').find('.selected').parent().addClass('ui-state-active');
};

var enableGlobalTabs = function() {
    removeRule('#portal-globalnav', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav', 'background-position', 'backgroundPosition');
    removeRule('#portal-globalnav', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-globalnav', 'background-image', 'backgroundImage');

    removeRule('#portal-globalnav li a', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav li a', 'background-position', 'backgroundPosition');
    removeRule('#portal-globalnav li a', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-globalnav li a', 'background-image', 'backgroundImage');

    removeRule('#portal-globalnav .selected a, #portal-globalnav a:hover', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav .selected a, #portal-globalnav a:hover', 'background-position', 'backgroundPosition');
    removeRule('#portal-globalnav .selected a, #portal-globalnav a:hover', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-globalnav .selected a, #portal-globalnav a:hover', 'background-image', 'backgroundImage');

    removeRule('#portal-globalnav .selected a, #portal-globalnav a:focus, #portal-globalnav a:hover', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav .selected a, #portal-globalnav a:focus, #portal-globalnav a:hover', 'color', 'color');
    removeRule('#portal-globalnav .selected a:focus, #portal-globalnav .selected a:hover', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav .selected a:focus, #portal-globalnav .selected a:hover', 'color', 'color');

    removeRule('#portal-globalnav .selected a:hover', 'background-color', 'backgroundColor');
    removeRule('#portal-globalnav .selected a:hover', 'background-position', 'backgroundPosition');
    removeRule('#portal-globalnav .selected a:hover', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-globalnav .selected a:hover', 'background-image', 'backgroundImage');
    removeRule('#portal-globalnav .selected a:hover', 'color', 'color');

    removeRule('#portal-globalnav .selected a, #portal-globalnav a:hover', 'color', 'color');

    $('<div id="ui-globalnav" class="ui-bottonset"></div>').insertBefore('#portal-globalnav');
    $('#portal-globalnav').appendTo('#ui-globalnav');

    $('#portal-globalnav').addClass('ui-state-default ui-corner-all');
    $('#portal-globalnav li').addClass('ui-button ui-widget ui-state-default ui-botton-text-only').css('border', '0px solid black').hover(function() {
        $(this).addClass('ui-state-hover');
    }, function() {
        $(this).removeClass('ui-state-hover');
    });
    $('#portal-globalnav li:first').addClass('ui-corner-left');
    $('#portal-globalnav li a').addClass('ui-button-text');
    $('#portal-globalnav').find('.selected').addClass('ui-state-active');
};

var enablePortlets = function() {
    removeRule('dl.portlet dt, div.portletAssignments div.portletHeader', 'background-color', 'backgroundColor');
    removeRule('dl.portlet dt, div.portletAssignments div.portletHeader', 'background-position', 'backgroundPosition');
    removeRule('dl.portlet dt, div.portletAssignments div.portletHeader', 'background-repeat', 'backgroundRepeat');
    removeRule('dl.portlet dt, div.portletAssignments div.portletHeader', 'background-image', 'backgroundImage');

    // special navportlet styling
    removeRule('div.managePortletsLink, a.managePortletsFallback', 'background-color', 'backgroundColor');
    removeRule('div.managePortletsLink, a.managePortletsFallback', 'background-position', 'backgroundPosition');
    removeRule('div.managePortletsLink, a.managePortletsFallback', 'background-repeat', 'backgroundRepeat');
    removeRule('div.managePortletsLink, a.managePortletsFallback', 'background-image', 'backgroundImage');
    $('dl.portlet ul.navTree .navTreeCurrentItem').removeClass('navTreeCurrentItem').css('font-weight', 'bold');

    // special calendar styling
    // TODO: apply this after kss request
    $('dl.portletCalendar .todaynoevent').removeClass('todaynoevent').addClass('ui-state-highlight');
    $('dl.portletCalendar .event').removeClass('event').addClass('ui-state-default');
    removeRule('.ploneCalendar .weekdays th', 'background-color', 'backgroundColor');

    removeRule('dl.portlet dt a:link, dl.portlet dt a:visited, dl.portlet dt a:hover', 'color', 'color');

    $('.portletHeader').addClass('ui-state-default ui-corner-all').removeClass('portletHeader');
    $('dl.portlet').addClass('ui-widget ui-widget-content ui-corner-all ui-helper-reset');
    $('dl.portlet dt').css('margin', '4px')
    $('.managePortletsLink').button();
};

var enableFooter = function() {
    removeRule('#portal-footer', 'background-color', 'backgroundColor');
    removeRule('#portal-footer', 'background-position', 'backgroundPosition');
    removeRule('#portal-footer', 'background-repeat', 'backgroundRepeat');
    removeRule('#portal-footer', 'background-image', 'backgroundImage');

    $('#portal-footer').addClass('ui-state-active ui-corner-all');
};

var edit_bar_interval = null;
var enableEditBar = function() {
    removeRule('#edit-bar', 'background-color', 'backgroundColor');
    removeRule('#edit-bar', 'border-left-color-value', 'borderLeftColor');
    removeRule('#edit-bar', 'border-left-width-value', 'borderLeftWidth');
    removeRule('#edit-bar', 'border-right-color-value', 'borderRightColor');
    removeRule('#edit-bar', 'border-right-width-value', 'borderRightWidth');
    removeRule('#edit-bar', 'border-left-color', 'borderLeftColor'); // needed for chrome
    removeRule('#edit-bar', 'border-left-width', 'borderLeftWidth'); // needed for chrome
    removeRule('#edit-bar', 'border-right-color', 'borderRightColor'); // needed for chrome
    removeRule('#edit-bar', 'border-right-width', 'borderRightWidth'); // needed for chrome
    removeRule('#edit-bar', 'border-top-color', 'borderTopColor');
    removeRule('#edit-bar', 'border-top-width', 'borderTopWidth');
    removeRule('#edit-bar, #content ul.formTabs', '-moz-border-radius-topleft', 'MozBorderRadiusTopleft');
    removeRule('#edit-bar, #content ul.formTabs', '-moz-border-radius-topright', 'MozBorderRadiusTopright');

    // left actions
    removeRule('#content-views', 'background-color', 'backgroundColor');
    removeRule('#content-views a', 'color', 'color');
    removeRule('#content-views li.selected a, #content-views li a:hover, #content li.formTab a.selected, #content li.formTab a:hover', 'background-color', 'backgroundColor');
    removeRule('#content-views li.selected a, #content-views li a:hover, #content li.formTab a.selected, #content li.formTab a:hover', 'background-image', 'backgroundImage');
    removeRule('#content-views li.selected a, #content-views li a:hover, #content li.formTab a.selected, #content li.formTab a:hover', 'background-position', 'backgroundPosition');
    removeRule('#content-views li.selected a, #content-views li a:hover, #content li.formTab a.selected, #content li.formTab a:hover', 'color', 'color');

    // right actions
    removeRule('#contentActionMenus', 'background-color', 'backgroundColor');
                
    removeRule('#contentActionMenus dl.actionMenu a, #contentActionMenus dl.actionMenu.activated dd', 'background-color', 'backgroundColor');
    removeRule('#contentActionMenus dl.actionMenu a, #contentActionMenus dl.actionMenu.activated dd', 'color', 'color');

    removeRule('#contentActionMenus dl.actionMenu.activated dd', 'border-bottom-color', 'borderBottomColor');
    removeRule('#contentActionMenus dl.actionMenu.activated dd', 'border-bottom-style', 'borderBottomStyle');
    removeRule('#contentActionMenus dl.actionMenu.activated dd', 'border-bottom-width', 'borderBottomWidth');

    removeRule('#contentActionMenus dl.actionMenu.activated dd a:focus, #contentActionMenus dl.actionMenu.activated dd a:hover, #contentActionMenus dl.actionMenu.activated dd .actionMenuSelected', 'background-color', 'backgroundColor');
    removeRule('#contentActionMenus dl.actionMenu.activated dd a:focus, #contentActionMenus dl.actionMenu.activated dd a:hover, #contentActionMenus dl.actionMenu.activated dd .actionMenuSelected', 'color', 'color');
    removeRule('#contentActionMenus dl.actionMenu a:focus, #contentActionMenus dl.actionMenu a:hover', 'color', 'color');

    edit_bar_interval = window.setInterval('enableEditBar2()', 100);
}

var enableEditBar2 = function() {
    if ($('#edit-bar').length) {
	window.clearInterval(edit_bar_interval);

	// using inverted colors
	$('#edit-bar').addClass('ui-state-active ui-corner-top');
	$('#content-views li.selected a').addClass('ui-state-default');
	$('#content-views li a').hover(function() {
	    $(this).addClass('ui-state-hover');
	}, function() {
	    $(this).removeClass('ui-state-hover');
	});

	$('#contentActionMenus dd.actionMenuContent').addClass('ui-state-active ui-corner-bottom').css('right', '-1px').css('border-top', '0px').css('padding', '2px');
	$('#contentActionMenus dl.actionMenu').hover(function() {
	    $(this).addClass('ui-state-hover ui-corner-top').css('border', '0px');
	}, function() {
	    $(this).removeClass('ui-state-hover ui-corner-top');
	});

	$('#contentActionMenus a.actionMenuSelected').addClass('ui-state-default ui-corner-all');
	$('#contentActionMenus a').hover(function() {
	    $(this).addClass('ui-state-hover ui-corner-all').css('border', '0px');
	}, function() {
	    $(this).removeClass('ui-state-hover ui-corner-all');
	});
    }
}
