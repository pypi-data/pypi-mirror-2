"""

    Functions useful when developing/debugging code.

"""


__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__author_url__ = "http://www.twinapex.com"
__docformat__ = 'epytext'
__copyright__ = "2010 Twinapex Research"
__license__ = "GPL v2"

def debug_layers(context):
    """
    Print all active browser layerse.
    """
    from zope.component import adapts
    from zope.component import getSiteManager
    from zope.component import queryMultiAdapter
    from zope.component import getSiteManager
    from zope.component import getAllUtilitiesRegisteredFor

    from plone.browserlayer.interfaces import ILocalBrowserLayerType
    from plone.browserlayer.utils import register_layer, unregister_layer
    
    active = context.REQUEST.__provides__.__iro__
    print active
