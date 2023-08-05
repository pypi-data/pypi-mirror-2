"""
    Support behavior assignments for non-dexerity objects.

    Make dummy assumption that all contentish objects support all behaviors.
    
"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>'
__docformat__ = 'epytext'
__copyright__ = "2010 mFabrik Research Oy"
__license__ = "GPL v2"

import zope.interface
import zope.component
from plone.behavior.interfaces import IBehavior, IBehaviorAssignable

from Products.CMFCore.interfaces import IContentish

class ATBehaviorAssignable(object):
    """ Dummy policy which allows you to place headers on every content object.

    TODO: This probably conflicts with everything else, but plone.behavior didn't provide
    documentation how assignables and Plone are related.
    """
    
    zope.interface.implements(IBehaviorAssignable)

    def __init__(self, context):
        self.context = context

    def supports(self, behavior_interface):
        return True

