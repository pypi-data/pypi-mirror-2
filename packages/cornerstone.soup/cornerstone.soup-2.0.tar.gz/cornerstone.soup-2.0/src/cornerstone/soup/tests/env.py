# Copyright 2009-2010, BlueDynamics Alliance - http://bluedynamics.com
from zope.interface import implements
from zope.catalog.catalog import Catalog
from zope.catalog.field import FieldIndex
from cornerstone.soup.interfaces import ICatalogFactory

class MyCatalogFactory(object):
    """ICatalogFactory implementation used for testing.
    """

    implements(ICatalogFactory)
    
    catalog = Catalog()
    catalog[u'user'] = FieldIndex(field_name='user',
                                  field_callable=False)

    def __call__(self):
        return self.catalog