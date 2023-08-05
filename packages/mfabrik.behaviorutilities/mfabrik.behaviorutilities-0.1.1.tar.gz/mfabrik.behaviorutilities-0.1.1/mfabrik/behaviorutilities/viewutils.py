"""

    Various view helper functions.

    Note that methods here are probably an overkill,
    unless you want to have specific tracebacks *which*
    view was not found.
   
    http://mfabrik.com 

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>'
__docformat__ = 'epytext'
__copyright__ = "2010 Twinapex Research"
__license__ = "GPL v2"



def getView(context, name):
    """ Get Zope 2 view with acquisition chain properly set up.

    A helpful exception message is provided which view failed to resolve.

    @param context: Context for which the view is looked for
    
    @param name: Attribute name holding the view name
    
    @raise: RuntimeError if view does not exist
    
    @return: View instance
    """

    try:
        view = context.unrestrictedTraverse("@@" + name)
    except AttributeError:
        raise RuntimeError("Instance %s did not have view %s" % (str(context), name))

    view = view.__of__(context)

    return view

def queryView(context, name):
    """ Query Zope 2 view with acquisition chain properly set up.

    @param name: Attribute name holding the view name
    
    @return: View instance or None if view does not exist
    """


    try:
        view = context.unrestrictedTraverse("@@" + name)
    except AttributeError:
        return None

    view = view.__of__(context)

    return view


from zope.component import getMultiAdapter

def getSiteRootRelativePath(context, request):
    """ Get site root relative path to an item
    
    @param context: Content item which path is resolved
    
    @param request: HTTP request object
    
    @return: Path to the context object, relative to site root, prefixed with a slash.
    """
    
    portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
    site = portal_state.portal()
    
    # Both of these are tuples 
    site_path = site.getPhysicalPath();
    context_path = context.getPhysicalPath()
    
    relative_path = context_path[len(site_path)+1:]
    
    return "/" + "/".join(relative_path)
    