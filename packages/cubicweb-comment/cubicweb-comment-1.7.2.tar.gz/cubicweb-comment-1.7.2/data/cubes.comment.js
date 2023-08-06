/*
 *  :organization: Logilab
 *  :copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
 *  :contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
 */

/* this function is called on inlined-comment editions
 * It calls the [add|eid]_comment method on the jsoncontroller and [re]load
 * only the view for the added or edited comment
 */
function processComment(eid, cancel, creation) {
    var divId = 'comment' + eid + 'Slot';
    var divNode = jQuery('#'+divId);
    var textarea = divNode.find('textarea')[0];
    if (!cancel) {
	validateForm('commentForm' + eid, null,
		     function(result, formid, cbargs) {
			 var neweid = result[2].eid;
			 if (creation) {
			     var commentNode = $('#comment'+ eid);
			     var ul = null;
			     if (!commentNode.length) {
				 // we are adding a comment to the top level entity
				 commentNode = $('#commentsection' + eid);
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
			 }
			 var form = ajaxFuncArgs('render', null, 'views', 'treeitem', neweid);
			 $('#comment' + neweid + 'Div').loadxhtml('json', form, null, null, true);
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
