Overview
========

``cornerstone.soup`` provides a container for persistent records which are
queryable. It is a genric storage for mass-data in an isolated container. 
Light-weight records are stored in an ``IOBTree``. A Zope-Tool-Kit catalog in 
used to index values of interest. cornerstone.soup  is no out-of-the-box 
package. Its addressed to developers needing to solve the problem of storing 
tiny entities of mass-data, where heavy weight archetypes or dexterity are too 
much effort and are to slow. I.e if you need a container for non-CMSish content, 
like votes, data from a poll, orders in a webshop, measuring data, or alike.

Updating
========

In earlier days of this package we thought it's a good idea to persist the
soup data in persistent local components. That was quite a mistake, at least
in Plone context, because GenericSetup purges local components when applying
base profiles - what you're normally not doing, but experience shows that shit
happens ;). So we changed the storage location to annotations on an acquireable,
``ISoupAnnotatable`` providing context.

Further the soup API was designed as utility, which was basically a good idea,
but caused toubles when looking up ``SoupData`` after the storage change.
We used ``getSiteManager`` to access the Acquisition context, and encountered
inconsistencies for accessing the Acquisition context from different site
managers in Plone.

The second problem forced us more or less to abandon the utility pattern, the
soup object itself now acts as adapter for context and is looked up via
``getSoup`` instead of a utility lookup. After updating, you'll get
``NoLongerSupported`` errors when trying to access a soup which is provided and
looked up as utility. You'll have to change your code to use ``getSoup``,
and remove the soup local component registration from your GS Profile(s).
::

    >>> from cornerstone.soup import getSoup
    >>> soup = getSoup(context, 'mysoup')

The new package ships with data migration. After updating call
``soup-controlpanel`` (in Plone) and run storage migration and remove persistent
local component for each soup. Prior to running the storage migration the 
existing soup data is inaccessible.

Due to the fact that the soup was originally persisted to the ZOBD, it still
inherits from SimpleItem. This will be changed with the release 3.0.
Keep in mind that 3.0 will break installations with non-cleaned-up
installations.

Usage
=====

``SoupData`` objects are stored as annotation to an object providing the
``ISoupAnnotatable`` interface.

For use inside Plone, provide ``ISoupAnnotatable`` via ``five.implements`` on
the plone site object usind ZCML.
::

    <five:implements
        class="Products.CMFPlone.Portal.PloneSite"
        interface="cornerstone.soup.interfaces.ISoupAnnotatable" />

``SoupData`` is looked up by ``id`` for a given context. This context acquires
it's parent until ``ISoupAnnotatable`` is found, on which the ``SoupData`` is
annotated by ``id``. Use ``getSoup`` function for this.
::

    >>> from cornerstone.soup import getSoup
    >>> soup = getSoup(context, 'my_soup_id')
    >>> soup
    <Soup at my_soup_id>

If no ``SoupData`` is found for given id, a new one is created and annotated
to ``ISoupAnnotatable``.

We must provide an ``ICatalogFactory`` implementation for each soup, registered
as utility under the same ``id`` as ``SoupData`` is annotated.
::

    >>> from zope.interface import implements
    >>> from zope.catalog.catalog import Catalog
    >>> from zope.catalog.field import FieldIndex
    >>> from cornerstone.soup.interfaces import ICatalogFactory
    >>> class MyCatalogFactory(object):
    ...     implements(ICatalogFactory)
    ...
    ...     def __call__(self):
    ...         catalog = Catalog()
    ...         catalog[u'name'] = FieldIndex(field_name='name',
    ...                                       field_callable=False)
    ...         return catalog

ZCML.
::

    <utility
        name="my_soup_id"
        factory=".mymodule.MyCatalogFactory"
        provides="cornerstone.soup.interfaces.ICatalogFactory" />

A Soup can only contain ``Records``. A Record is a simple persistent object
which accepts any keyword arguments on ``__init__`` time. This arguments are 
used as Record properties.

Create a Record and add it to soup.
::

    >>> from cornerstone.soup import Record
    >>> record = Record(user='user1')
    >>> id = soup.add(record)

Check querying.
::

    >>> [r for r in soup.query(user='user1')]
    [<Record at ...>]
    
    >>> [r for r in soup.query(user='nonexist')]
    []
    
Add some more Records.
::

    >>> id = soup.add(Record(user='user1'))
    >>> id = soup.add(Record(user='user2'))
    >>> u1records = [r for r in soup.query(user='user1')]
    >>> u1records
    [<Record at ...>, 
    <Record at ...>]

Change user attribute of one record.
::

    >>> u1records[0].data['user'] = 'user2'

The query still returns the old result. The Record must be reindexed.
::

    >>> [r for r in soup.query(user='user1')]
    [<Record at ...>, 
    <Record at ...>]
    
    >>> soup.reindex([u1records[0]])
    
    >>> u1 = [r for r in soup.query(user='user1')]
    >>> u1
    [<Record at ...>]
    
    >>> u2 = [r for r in soup.query(user='user2')]
    >>> u2
    [<Record at ...>, 
    <Record at ...>]

You can reindex all records in soup at once.
::

    >>> all = [r for r in soup.data.values()]
    >>> all = sorted(all, key=lambda x: x.user)
    >>> all
    [<Record at ...>, 
    <Record at ...>, 
    <Record at ...>]
    
    >>> all[-1].data['user'] = 'user3'
    >>> soup.reindex()
    >>> [r for r in soup.query(user='user3')]
    [<Record at ...>]

You can also rebuild the catalog. In this case the catalog factory is called
again and the new catalog is used. Lets modify catalog of catalog factory.
::

    >>> from zope.catalog.field import FieldIndex
    >>> catalogfactory = getUtility(ICatalogFactory, name='mysoup')
    >>> catalogfactory.catalog[u'name'] = FieldIndex(field_name='name',
    ...                                   field_callable=False)
    >>> catalogfactory()[u'name']
    <zope.catalog.field.FieldIndex object at ...>

Set name attribute on some record data, rebuild soup and check results.
::

    >>> all[0].data['name'] = 'name'
    >>> all[1].data['name'] = 'name'
    >>> all[2].data['name'] = 'name'
    >>> soup.rebuild()
    >>> [r for r in soup.query(name='name')]
    [<Record at ...>, 
    <Record at ...>, 
    <Record at ...>]
    

Delete records.
::

    >>> del soup[all[0]]
    >>> [r for r in soup.query(name='name')]
    [<Record at ...>, 
    <Record at ...>]

For huge expected results we can query LazyRecords. They return the real record
on call.
::

    >>> lazy = [l for l in soup.lazy(name='name')]
    >>> lazy
    [<cornerstone.soup.soup.LazyRecord object at ...>, 
    <cornerstone.soup.soup.LazyRecord object at ...>]
    
    >>> lazy[0]()
    <Record at ...>

TODO
====

* extend soup API by ``clear()`` function.

Contributors
============

  * Robert Niederreiter <rnix@squarewave.at>
  * Jens Klein <jens@bluedynamics.com>
