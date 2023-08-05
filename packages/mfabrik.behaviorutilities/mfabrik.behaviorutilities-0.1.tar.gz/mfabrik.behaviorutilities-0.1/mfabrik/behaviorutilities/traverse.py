"""

    Various traverse utilities.

    http://mfabrik.com
"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>'
__docformat__ = 'epytext'
__copyright__ = "2010 mFabrik Research Oy"
__license__ = "GPL v2"

from Products.CMFCore.interfaces import ISiteRoot

def getParents(object):
    """ Get object parents as iterable.

    Example::

        parents = getParents(self.context)
        print "I have parents:" + str(list(parents))
        

    @param object: Any content object
    @return: Iterable of all parents from the direct parent to the site root
    """

    # It is important to use inner to bootstrap the traverse,
    # or otherwise we might get surprising parents
    # E.g. the context of the view has the view as the parent
    # unless inner is used
    inner = object.aq_inner

    # Return nothing if we are alare at the site root 
    if not ISiteRoot.providedBy(inner):

        parent = inner.aq_parent
        while not ISiteRoot.providedBy(parent):        
            
            yield parent
    
            if not hasattr(parent, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(parent))
    
            parent = parent.aq_parent

def getAcquisitionChain(object):
    """
    @return: List of objects from context, its parents to the portal root

    Example::

        chain = getAcquisitionChain(self.context)
        print "I will look up objects:" + str(list(chain))

    @param object: Any content object
    @return: Iterable of all parents from the direct parent to the site root
    """

    # It is important to use inner to bootstrap the traverse,
    # or otherwise we might get surprising parents
    # E.g. the context of the view has the view as the parent
    # unless inner is used
    inner = object.aq_inner

    iter = inner

    while iter:
        yield iter

        if ISiteRoot.providedBy(iter):
           break

        if not hasattr(iter, "aq_parent"):
            raise RuntimeError("Parent traversing interrupted by object: " + str(parent))

        iter = iter.aq_parent
