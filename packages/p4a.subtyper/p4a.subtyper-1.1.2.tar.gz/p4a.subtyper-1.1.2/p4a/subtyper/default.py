from Acquisition import aq_inner
from zope.interface import implements, implementer, Interface
#import zope.component
from zope.component import getUtilitiesFor, adapter

import Products.Archetypes.interfaces
from p4a.subtyper import interfaces


class PossibleDescriptors(object):
    implements(interfaces.IPossibleDescriptors)

    def __init__(self, possible=[], comment=None):
        self._possible = possible
        self._comment = comment

    @property
    def possible(self):
        return self._possible

    def __str__(self):
        return '<PossibleDescriptors comment=%s>' % (self._comment or '')
    __repr__ = __str__


@adapter(Products.Archetypes.interfaces.IBaseFolder)
@implementer(interfaces.IPossibleDescriptors)
def folderish_possible_descriptors(context):
    portal_type = getattr(aq_inner(context), 'portal_type', None)
    if portal_type is None:
        return PossibleDescriptors()

    possible = getUtilitiesFor(\
               interfaces.IPortalTypedFolderishDescriptor)
    return PossibleDescriptors([(n, c) for n, c in possible
                                if c.for_portal_type == portal_type],
                               'folderish')


@adapter(Interface)
@implementer(interfaces.IPossibleDescriptors)
def nonfolderish_possible_descriptors(context):
    portal_type = getattr(aq_inner(context), 'portal_type', None)
    if portal_type is None:
        return PossibleDescriptors()

    all = getUtilitiesFor(\
          interfaces.IPortalTypedDescriptor)
    folderish = getUtilitiesFor(\
          interfaces.IPortalTypedFolderishDescriptor)

    all = set([(n, c) for n, c in all if c.for_portal_type == portal_type])
    folderish = set([(n, c) for n, c in folderish
                     if c.for_portal_type == portal_type])

    return PossibleDescriptors(list(all.difference(folderish)),
                               'nonfolderish')
