Introduction
============

This is a simple product that patches the ZCatalog such that you can register sort adapters for results.

The main usecase for this is to tailor search results to specific business rules, eg. 'Recent document are more important than old'
or 'Documents from the CEO are more important than from the tea boy'.

To use it you need to write a utility that provides a sorted() method that can be passed
a LazyMap of brains and re-score and re-sort them based upon your criteria.

See adapters.py for some examples.


