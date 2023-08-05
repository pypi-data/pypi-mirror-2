/*
 *  :organization: Logilab
 *  :copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
 *  :contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
 */

CubicWeb.require('python.js');
CubicWeb.require('htmlhelpers.js');
CubicWeb.require('ajax.js');

function _getText(textarea) {
    if (typeof(FCKeditor) != 'undefined') {
        var fck = FCKeditorAPI.GetInstance(textarea.id);
        if (fck) {
            return fck.GetHTML();
        }
    }
    return textarea.value;
}

/* this function is called on inlined-comment editions
 * It calls the [add|eid]_comment method on the jsoncontroller and [re]load
 * only the view for the added or edited comment
 */
function processComment(eid, funcname, creation) {
    var divId = 'comment' + eid + 'Slot'
    var divNode = jQuery('#'+divId);
    var textarea = divNode.find('textarea')[0];
    if (funcname) {
        var format = 'text/html'; // no select widget if fckeditor is used
        var select = divNode.find('select')[0];
        if (select) {
            format = firstSelected(select);
        }
        d = asyncRemoteExec(funcname, eid, _getText(textarea), format);
        d.addCallback(function (neweid) {
	    if (creation) {
		var commentNode = jQuery('#comment'+ eid);
		var ul = null;
		if (!commentNode.length) {
		    // we are adding a comment to the top level entity
		    commentNode = jQuery('#commentsectionComponent');
		    klass = 'comment';
		} else {
		    klass = 'section';
		}
		ul = commentNode.find('> ul:first');
		if (!ul.length) {
		    ul = jQuery(UL({'class': klass}));
		    commentNode.append(ul);
		}
		ul.append(LI({'id': 'comment'+ neweid, 'class': 'comment'},
			     DIV({'id': 'comment'+ neweid + 'Div'})));
		divNode.remove();
		eid = neweid;
	    }
	    replacePageChunk('comment' + eid + 'Div', rql_for_eid(eid), 'treeitem');
        });
    } else {
	// comment cancelled, close div holding the form
        divNode.remove();
	// on edition, show back the comment's content
	if (!creation) {
	    jQuery('#comment' + eid + 'Div div').show();
	}
    }
}

function showLoginBox() {
    toggleVisibility('popupLoginBox');
    $('html, body').animate({scrollTop:0}, 'fast');
    return false;
}

CubicWeb.provide('comment.js');

