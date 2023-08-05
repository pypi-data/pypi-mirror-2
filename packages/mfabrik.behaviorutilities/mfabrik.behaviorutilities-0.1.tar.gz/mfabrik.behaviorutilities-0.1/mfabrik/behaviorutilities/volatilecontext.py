"""
    An persistent object helper pattern with following properties
    
    - Default schema values is used as long one save() is expilicitly called -
      this is to prevent database overload for creating new behaviors 
      for every database object loaded / created
      
    - Play nice with z3c.form vocabularies (context hack)

"""

__author__  = 'Mikko Ohtamaa <mikko.ohtamaa@mfabrik.com>'
__docformat__ = 'epytext'
__copyright__ = "2010 mFabrik Research Oy"
__license__ = "GPL v2"

import zope.interface

from zope.annotation import IAnnotations
from zope import schema

from persistent import Persistent

class IVolatileContext(zope.interface.Interface):
    """ """

    context = schema.Object(zope.interface.Interface, description=u"Run-time reference accessor to the parent object this object belongs to")

    factory = schema.Object(zope.interface.Interface, description=u"Reference to the factory which created this run-time instance")

    def save():
        """ Write object to the database and construct connection with the parent object.
        """
        
class VolatileContext(Persistent):
    """ Mix-in class to provide non-persistent context  to persistent classes.

    Some subsystems (e.g. z3c.forms) expect objects to have a context reference to parent/site/whatever.
    However, storing this back-reference persistenly is not needed, as the factory
    method will always know the context.

    This helper class creates a context property which is volatile (never persistent),
    but can be still set on the object after creation or after database load.
    """

    zope.interface.implements(IVolatileContext)

    @property
    def context(self):
        return self._v_context

    @property
    def factory(self):
        return self._v_factory

    # http://docs.python.org/library/functions.htm
    def save(self):
        """ """
        self.factory.makePersistent(self)

class AnnotationPersistentFactory(object):
    """ A factory pattern to manufacture persistent objects stored within the parent object annotations.

    Until the first write, the default (non-persistent) object is return. This prevents
    possible situations where database read could cause write.

    The first write must call AnnotationPersistentFactory.makePersistent(object).
    Alternative, you can call AnnotationPersistentFactory.makePersistent(object)
    when entering the editing interface for the first time.

    After the first write, the saved persistent object is return.
    """


    def __init__(self, persistent_class, key):
        """
        @param persistent_class: Class reference / factory method which will create new objects.
            Created classes must conform VolatileContext interface

        @param key: ASCII string, Key name used with IAnnotations
        """
        self.persistent_class = persistent_class
        self.key = key
        self._assertProperlySetUp()

    def _assertProperlySetUp(self):
        """
        Check that the framework is properly set up
        """
        assert callable(self.persistent_class), "Factory is missing"

        assert hasattr(self.persistent_class, "context"), "The persistent object must support volatile context interface"

        assert self.key is not None, "You must give the annotations key"

    def makePersistent(self, object):
        """ Write created persistent object to the database.

        This will store the object on the annotations of its context.
        """
        assert isinstance(object, self.persistent_class), "Object %s was not type of %s" % (str(object), str(self.persistent_class))
        annotations = IAnnotations(object.context)
        annotations[self.key] = object

    def __call__(self, context):
        """ Called by Zope framework when doing a factory call.

        Usually this class is refered as <adapter factory=""> and
        this method creates a new, read-only, persistent object.
        """

        annotations = IAnnotations(context)

        if not self.key in annotations:
            # Construct a new (default) instance
            object = self.persistent_class()
        else:
            # Return the object stored previously
            object = annotations[self.key]

        # Set volatile context reference
        object._v_context = context
        object._v_factory = self

        return object


