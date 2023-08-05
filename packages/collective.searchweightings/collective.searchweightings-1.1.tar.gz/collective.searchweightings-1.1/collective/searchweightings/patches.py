from Products.ZCatalog.ZCatalog import ZCatalog
from zope.component import queryUtility
from interfaces import ICatalogSorter

def wrappedSearchResults(self, REQUEST=None, **kw):
    res = self._old_searchResults(REQUEST, **kw)

    sorter = queryUtility(ICatalogSorter)
    if sorter is not None:
        return sorter.sorted(res)

    return res
