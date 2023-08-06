var LinkCollection = { };
// Height of the tallest document which has been displayed
LinkCollection.maxheight = 0;

LinkCollection.render_doc = function render_doc(node, uid) {
    jq('a.current-linklist-item').removeClass('current-linklist-item');
    jq(node).addClass('current-linklist-item');
    jq('li.current').removeClass('current');
    jq(node.parentNode).addClass('current');

    jq('div.prefetched-docs').each(
	function(i){
	    if (jq(this).is(':visible')) {
		jq(this).hide();
	    }
	}
    );

    var doc = jq('div#doc-'+uid);
    doc.fadeIn(300);

    /* Prevent the page from jumping up and down for long and short
    documents by setting the height of the current doc to the
    height of the largest doc displayed so far. */
    /* I'm deactivating this, because I consider it harmful. If you view a long
    page, then a very short one, the footer will not be visible. Valuable links
    might not be accessible.
    Besides, the "page jumping" only seems to happen in FF, not in
    Safari, Chrome and Opera.
    Wolfgang Thomas 11.11.2010 */
    /* if (doc.height() > LinkCollection.maxheight) {
     LinkCollection.maxheight = doc.height();
    }
    doc.height(LinkCollection.maxheight); */

    // Scroll to the top of the linkbox
    var linkbox=jq('div#slc-linkcollection-linkbox');
    var linkboxtop=linkbox.offset().top;
    var body=jq('html,body');
    body.scrollTop(linkboxtop);
    return false;
}
