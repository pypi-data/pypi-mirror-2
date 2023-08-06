dojo.require('dojo.NodeList-traverse');
dojo.require('dojo.fx.easing');
dojo.require('dojo.window');
dojo.require('dojo.hash');

dojo.setObject('EventHandlers', {
    /**
     * If all tabs are closed, we will show the footer otherwise we
     * hide it
     */

    /**
     * When a folder tab is clicked, we will expand the contents
     */
    openOrCloseFolder: function(event) {
        if (event) {
            dojo.stopEvent(event);
        }

        var node = dojo.NodeList(event.currentTarget);
        var article = node.closest('article')[0];
        var h1 = node.children('h1')[0];

        EventHandlers.skipNextHashChange = true;

        Helper.toggleArticle(article);
        Helper.showOrHideFooter();

        dojo.hash(dojo.attr(h1, 'rel'));
    },

    /**
     * When a link to another document is clicked, we will expand the appropriate tab
     * and scroll to that document
     *
     * Links look like this:
     *     <a href="link" role="doc-link">Title</a>
     */
    navigateToDocument: function(event) {
        dojo.stopEvent(event);

        var currentTarget = event.currentTarget;
        var link = dojo.attr(currentTarget, 'href');

        Helper.clearHash();
        dojo.hash(link);
    },

    /**
     * Does the next hash change need to be ignored?
     */
    skipNextHashChange: false,

    /**
     * Expands a folder and scrolls to it
     */
    expandAndScrollArticle: function(link) {
        if (EventHandlers.skipNextHashChange) {
            // Skip, but get the next one ready
            EventHandlers.skipNextHashChange = false;
            return;
        }

        if (!arguments.length) {
            link = dojo.hash();
        }

        var target = dojo.query("article.folder div.tab h1[rel='" + link + "']")[0];

        Helper.openTabAndScrollTo(target);
        Helper.showOrHideFooter();
    }
});

dojo.setObject('Helper', {
    /**
     * Stores the original position information for the footer to be used
     * later when we are showing or hiding it
     */
    footerPosition: null,

    /**
     * Expands or closes the article
     */
    toggleArticle: function(article, setOpen) {
        article = dojo.NodeList(article);
        var method = dojo.toggleClass;

        if (setOpen === false) {
            method = dojo.removeClass;
        } else if (setOpen == true) {
            method = dojo.addClass;
        }

        var dl = article.children('dl')[0];
        var dt = dojo.query('dt', dl)[0];

        method(dl, 'expand');
        method(dt, 'open');
    },

    /**
     * Sets the hash to an empty string, so the next hash change event registers properly
     */
    clearHash: function() {
        EventHandlers.skipNextHashChange = true;
        dojo.hash('');
    },

    /**
     * Opens a tab and scrolls to it
     */
    openTabAndScrollTo: function(target) {
        if (!target) {
            return;
        }

        var targetNodeList = dojo.NodeList(target);
        var article = targetNodeList.closest('article')[0];

        Helper.toggleArticle(article, true);

        if (!article.scrollIntoView) {
            dojo.window.scrollIntoView(article);
        } else {
            article.scrollIntoView(true);
        }
    },

    /**
     * If all the tabs are closed, we can show the footer otherwise it needs to get out
     * of the way if a document is currently displayed
     */
    showOrHideFooter: function() {
        if (!Helper.footerPosition) {
            Helper.footerPosition = dojo.position(dojo.query('footer')[0])
        }

        var footer = dojo.query('footer')[0];

        var expanded = dojo.query('section.folders article.folder dl.expand');

        if (expanded.length == 0) {
            // Nothin is expanded, the footer should be displayed
            dojo.animateProperty({
                node: footer,
                properties: { bottom: 0 },
                easing: dojo.fx.easing.quadOut,
                duration: 200
            }).play();
        } else {
            // The footer is not back to it's reset position, let's not add another animation
            if (dojo.style(footer, 'bottom') != '0px') {
                return;
            }
            dojo.animateProperty({
                node: footer,
                properties: { bottom: (Helper.footerPosition.h * -0.9) },
                easing: dojo.fx.easing.quadOut,
                duration: 200
            }).play();
        }
    }
});

dojo.addOnLoad(function() {
    /**
     * When the folders are clicked, open their tabs and 
     */
    var tabLinkSelector = 'section.folders article.folder dt a';
    dojo.query(tabLinkSelector).forEach(function(node) {
        dojo.connect(node, 'onclick', EventHandlers.openOrCloseFolder);
    });

    /**
     * When links within the documents are clicked that refer to other docs
     * we will open that tab and scroll it into view
     */
    dojo.query('a[rel=doc-link]').forEach(function(node) {
        dojo.connect(node, 'onclick', EventHandlers.navigateToDocument);
    });

    /**
     * Listen for the hash tag to change, when it does we need to open the
     * appropriate tab and scroll that document into view
     */
    dojo.subscribe('/dojo/hashchange', EventHandlers.expandAndScrollArticle);

    if (hash = dojo.hash()) {
        EventHandlers.expandAndScrollArticle(hash);
    }

    /**
     * Alter the vieport if we are on a tablet
     */
    if (window.innerWidth >= 980) {
        // Appears we are on a tablet
        dojo.attr(dojo.byId("viewport"), 'content',
            'initial-scale=1.0, width=device-width, minimum-scale=1.0, maximum-scale=1.0');
    }
});
