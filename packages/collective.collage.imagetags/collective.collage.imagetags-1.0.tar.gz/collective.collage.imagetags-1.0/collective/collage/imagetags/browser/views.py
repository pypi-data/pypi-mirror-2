from Acquisition import aq_inner
from zope import interface, schema
from zope.component import getMultiAdapter, adapts
from z3c.form import form, field, button
from z3c.form.interfaces import HIDDEN_MODE
from plone.z3cform.layout import wrap_form
from zope.app.component.hooks import getSite
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements
from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.Collage.browser.views import BaseView
from Products.Collage.interfaces import ICollageAlias, ICollageEditLayer
from Products.ATContentTypes.interfaces import IATImage, IATNewsItem

from collective.collage.imagetags import message_factory as _
from collective.collage.imagetags.browser.interfaces import IImageTagsSettings

ANNOTATIONS_KEY = u'ImageTagsSettings'

_marker = object()
class AnnotatableFieldProperty(object):
    """Computed attributes based on schema fields

    Field properties provide default values, data validation and error messages
    based on data found in field meta-data.

    """

    def __init__(self, field, name=None):
        if name is None:
            name = field.__name__

        self.__field = field
        self.__name = name

    def __get__(self, inst, klass):
        if inst is None:
            return self
        inst = inst.context
        annotations = IAnnotations(inst)
        annotations = annotations.get(ANNOTATIONS_KEY, {})

        value = annotations.get(self._AnnotatableFieldProperty__name, _marker)
        if value is _marker:
            field = self._AnnotatableFieldProperty__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self._AnnotatableFieldProperty__name)

        return value

    def __set__(self, inst, value):
        inst = inst.context
        annotations = IAnnotations(inst)
        annotations =  annotations.setdefault(ANNOTATIONS_KEY, PersistentDict())

        field = self._AnnotatableFieldProperty__field.bind(inst)
        field.validate(value)
        if field.readonly:
            raise ValueError(self._AnnotatableFieldProperty__name, 'field is readonly')
        annotations[self._AnnotatableFieldProperty__name] = value

    def __getattr__(self, name):
        return getattr(self._AnnotatableFieldProperty__field, name)

class ImageTagsSettingsAdapter(object):
    """ Adapter for the IImageTagsSettings schema interface
    """
    implements(IImageTagsSettings)

    field = AnnotatableFieldProperty(IImageTagsSettings['field'])
    scale = AnnotatableFieldProperty(IImageTagsSettings['scale'])

    def __init__(self, context):
        self.context = context
    
class ImageTagsSettingsForm(form.EditForm):
    """ Form based on IImageTagsSettings
    """
    fields = field.Fields(IImageTagsSettings)
    #label = u"Imagetags settings"
    
    def updateWidgets(self):
        super(ImageTagsSettingsForm, self).updateWidgets()
        fields = self.widgets['field'].terms.terms._terms
        if len(fields)==1:
            self.widgets['field'].value = fields[0].value
            self.widgets['field'].mode = HIDDEN_MODE
        elif len(fields)==0:
            self.widgets['field'].mode = HIDDEN_MODE
           
    @button.buttonAndHandler(_(u'Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage
        context = self.context
        while context.Type() != 'Collage':
            context = context.aq_parent
        self.request.response.redirect(context.absolute_url() + '/compose')

ImageTagsSettings = wrap_form(ImageTagsSettingsForm)

class ImageTagsView(BaseView):
    """ Collage layout view to display tagged imgaes
    """
    
    title = _(u"Image tags")
    
    def __call__(self):
        template = ViewPageTemplateFile('templates/imagetags.pt')
        return template(self)
    
    def tagged_image(self):
        context = aq_inner(self.context)
        imagetags = getMultiAdapter((context, self.request), name="imagetags-img")
        data = IImageTagsSettings(self.collage_context)
        field_name = data.field
        
        if field_name is None:
            helper = getMultiAdapter((context, self.request), name="imagetags-helper")
            fields = helper.image_fields()
            if len(fields)>0:
                field_name = fields[0]
            else:
                # Report no image field available
                return self.report_error(_(u"Selected object has no image field"))
                
        try:
            field = context.getField(field_name)
            if field.get_size(context)==0:
                # Report image is empty (no image loaded)
                return self.report_error(_(u"Selected object has no loaded image"))
            scale = data.scale or 'original'
            if scale!='original':
                if scale in field.getAvailableSizes(context):
                    name = '%s_%s' % (field_name, scale)
                else:
                    # Report scale not found for given field
                    return self.report_error(_(u"Selected scale not available"))
            else:
                name = field_name
                
            return imagetags(name=name)
        except:
            # Report the error
            return self.report_error(_(u"Selected image not available"))

    def report_error(self, msg):
        if ICollageEditLayer.providedBy(self.request):
            msg = _(msg)
            return '<strong>%s</strong>' % (msg)
        else:
            return ''
