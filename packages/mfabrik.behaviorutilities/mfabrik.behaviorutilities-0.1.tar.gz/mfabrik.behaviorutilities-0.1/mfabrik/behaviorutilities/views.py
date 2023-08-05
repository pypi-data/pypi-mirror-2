"""

    TODO: This module is going to provide five.grok 
    based form base classes for behaviors.

"""

from Acquisition import aq_inner
import z3c.form.interfaces

from five import grok

from plone.z3cform import z2
from plone.z3cform import interfaces


def get_template_file(name):
    """
    Helper function to get a Grok template from this package.
    
    http://old.nabble.com/Viewlets-template-inheritance-broken-if-in-another-package--td25944725.html 
    """
    import sys, os
    module = sys.modules[__name__]
    path = os.path.basename(module.__file__)
    templates = os.path.join(path, "templates")
    file = os.path.join(templates, name)
    return file 
    
class Z3CFormView(grok.CodeView):
    """
    Grok compatible view to render z3c.forms in Plone.
    
    XXX: Couldn't get this ever work... 
    
    XXX: This is ugly. Please fix Grok soon.
    """
    
    grok.baseclass()

    # Set this to reference to a Z3C form object in a subclass
    form = None

    template = grok.PageTemplateFile("templates/z3cformview.pt")
    
    def label(self):
        return self.form_instance.label
    
    def update(self):
        """
        """
        z2.switch_on(self, request_layer=z3c.form.interfaces.IFormLayer)
        self.form_instance = self.form(aq_inner(self.context), self.request)

    def render(self):
        return self.template.render(self)
    
    # XXX: Copied from grokcore.view.components.View
    
    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        #namespace['static'] = self.static
        namespace['view'] = self
        return namespace

    def namespace(self):
        return {}