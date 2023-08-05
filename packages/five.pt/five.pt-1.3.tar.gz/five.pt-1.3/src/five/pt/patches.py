"""Monkey-patching page template classes.

Since many templates are instantiated at module-import, we patch using
a duck-typing strategy.

We replace the ``__get__``-method of the ViewPageTemplateFile class
(both the Five variant and the base class). This allows us to return a
Chameleon template instance, transparent to the calling class.
"""

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile as \
     ZopeViewPageTemplateFile

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.PageTemplateFile import PageTemplate
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as \
     FiveViewPageTemplateFile

from five.pt.pagetemplate import ViewPageTemplateFile
from five.pt.pagetemplate import BaseTemplate
from five.pt.pagetemplate import BaseTemplateFile

from Acquisition import aq_base
from Acquisition import aq_parent
from Acquisition.interfaces import IAcquirer
from Acquisition import ImplicitAcquisitionWrapper

from ComputedAttribute import ComputedAttribute

try:
    from Products.Five.browser.pagetemplatefile import BoundPageTemplate
except ImportError:
    from zope.app.pagetemplate.viewpagetemplatefile import BoundPageTemplate
    import Acquisition

    class BoundPageTemplate(BoundPageTemplate, Acquisition.Implicit):
        """Implementing Acquisition.interfaces.IAcquirer and
        IAcquisitionWrapper.
        """

        __parent__ = property(lambda self: self.im_self)

        def __call__(self, im_self=None, *args, **kw):
            if self.im_self is None:
                im_self = im_self
            else:
                im_self = aq_base(self.im_self)
                if IAcquirer.providedBy(im_self):
                    im_self = im_self.__of__(im_self.context)
            return self.im_func(im_self, *args, **kw)

    class BaseTemplateFile(BaseTemplateFile, Acquisition.Implicit):
        """Implement Acquisition.interfaces.IAcquirer and
        IAcquisitionWrapper.
        """

_marker = object()

def get_bound_template(self, instance, type):
    if instance is None:
        return self

    template = getattr(self, '_v_template', _marker)
    if template is _marker:
        self._v_template = template = ViewPageTemplateFile(self.filename)

    return BoundPageTemplate(template, instance)

def call_template(self, *args, **kw):
    template = getattr(self, '_v_template', _marker)
    if template is _marker or self._text != template.body:
        self._v_template = template = BaseTemplate(self._text)

    return template(self, *args, **kw)

def call_template_and_wrap(self, *args, **kw):
    template = getattr(self, '_v_template', _marker)
    if template is _marker or self._text != template.body:
        self._v_template = template = BaseTemplate(self._text)

    if IAcquirer.providedBy(template):
        template = template.__of__(aq_parent(self))
    else:
        template = ImplicitAcquisitionWrapper(template, aq_parent(self))

    return template(self, *args, **kw)

def call_template_file(self, *args, **kw):
    template = getattr(self, '_v_template', _marker)
    if template is _marker:
        self._v_template = template = BaseTemplateFile(self.filename)

    if IAcquirer.providedBy(template):
        template = template.__of__(aq_parent(self))
    else:
        template = ImplicitAcquisitionWrapper(template, aq_parent(self))

    return template(self, *args, **kw)

def get_macros(self):
    template = getattr(self, '_v_template', _marker)
    if template is _marker:
        self._v_template = template = BaseTemplateFile(self.filename)

    if IAcquirer.providedBy(template):
        return template.__of__(aq_parent(self)).macros
    else:
        return template.macros

FiveViewPageTemplateFile.__get__ = get_bound_template
ZopeViewPageTemplateFile.__get__ = get_bound_template
PageTemplate.__call__ = call_template
PageTemplate.macros = ComputedAttribute(get_macros, 1)
PageTemplateFile.__call__ = call_template_file
PageTemplateFile.macros = property(get_macros)
ZopePageTemplate.__call__ = call_template_and_wrap
ZopePageTemplate.macros = ComputedAttribute(get_macros, 1)

try:
    from five.grok.components import ZopeTwoPageTemplate

    class GrokViewAwarePageTemplateFile(ViewPageTemplateFile):

        def pt_getContext(self, instance, request, **kw):
            return {}
    
        def _pt_get_context(self, instance, request, kwargs={}):
            namespace = super(GrokViewAwarePageTemplateFile, self)._pt_get_context(
                instance, request, kwargs)
            if hasattr(self, 'pt_grokContext'):
                namespace.update(self.pt_grokContext)
            return namespace

        def pt_render(self, namespace):
            self.pt_grokContext = namespace
            # namespace contains self.pt_getContext() result + \
            # five.grok.components.ZopeTwoPageTemplate.getNamespace(view) result
            # we have currently context, request, static, and view in the dict
            view = namespace["view"]
            return self.__call__(_ob=view)
            # z3c.pt.pagetemplate.ViewPageTemplate.__call__ will call self._pt_get_context(ob, None, None)

    def setFromFilename(self, filename, _prefix=None):
        self._template = GrokViewAwarePageTemplateFile(filename, _prefix)
    ZopeTwoPageTemplate.setFromFilename = setFromFilename
except ImportError:
    pass

