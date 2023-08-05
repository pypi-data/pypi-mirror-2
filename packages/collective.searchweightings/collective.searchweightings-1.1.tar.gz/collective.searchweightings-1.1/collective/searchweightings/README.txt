Firstly we need to create some content:

>>> self.folder.invokeFactory('News Item', 'item1', title='News Item')
'item1'
>>> self.folder.invokeFactory('News Item', 'item2', title='Another News Item')
'item2'


Register our sorter as a utility
>>> from zope.component import getGlobalSiteManager
>>> from collective.searchweightings.interfaces import ICatalogSorter
>>> from collective.searchweightings.adapters import WeightedDateSorter
>>> gsm = getGlobalSiteManager()
>>> gsm.registerUtility(WeightedDateSorter(), ICatalogSorter)

Do a search:

>>> brains = self.portal.portal_catalog(SearchableText='News Item')
>>> [ b.getId for b in brains ]
['item1', 'item2']


Now lets set the modification time of item1 to be much older,
we should now get item2 being the first result
>>> from DateTime.DateTime import DateTime
>>> item1 = self.folder.item1
>>> item1.getField('modification_date').set(item1, DateTime('2006/01/01'))

We need to rebuild the catalog to make sure changes are in it
>>> self.portal.portal_catalog.refreshCatalog()

Item2 should now be the first item
>>> brains = self.portal.portal_catalog(SearchableText='News Item')
>>> [ b.getId for b in brains ]
['item2', 'item1']






