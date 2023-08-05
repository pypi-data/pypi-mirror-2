# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface
from zope.component import getUtility
from dolmen.app.layout import Page, master
from dolmen.app.search import ICatalogSearcher
from dolmen.app.search import MF as _

class Search(grok.Viewlet):
    grok.context(Interface)
    grok.name('search.viewlet')
    grok.viewletmanager(master.Top)
    grok.order(10)
    grok.require("dolmen.content.View")

    def update(self):
        self.term = self.request.form.get('search_term', u'')


class Results(Page):
    grok.context(Interface)
    grok.name('search.result')
    grok.require("dolmen.content.View")

    def update(self):
        searcher = getUtility(ICatalogSearcher, 'searcher.sitecatalog')
        term = self.request.form.get('search_term', u'')
        if term:
            self.results = searcher.search(term + '*')
        else:
            self.results = []
        mapping = {"number": len(self.results),
                   "searchterm": term}
        self.label = _("label_results_found",
                       mapping=mapping, 
                       default=u"Found %(number)s results for %(searchterm)s" % mapping)
