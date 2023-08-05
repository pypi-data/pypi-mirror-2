from zope.interface import Interface

class ICatalogSorter(Interface):

    """ A Catalog Sorter
    """

    def sorted(brains):
        """ take a LazyMap of brains, sort and return a LazyMap """
        pass
