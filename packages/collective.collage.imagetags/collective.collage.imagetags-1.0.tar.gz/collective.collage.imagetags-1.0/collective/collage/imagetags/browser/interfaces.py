from zope import interface, schema
from collective.collage.imagetags import message_factory as _

class IImageTagsSettings(interface.Interface):
    """ Settings for imagetags view for Collage
    """
    field = schema.Choice(title=_(u"Image field"),
                          description=_(u"Image field whose tags you want to display"),
                          vocabulary='collective.collage.imagetags.imagefields',
                          required=True)
                          
    scale = schema.Choice(title=_(u"Image scale"),
                          vocabulary='collective.collage.imagetags.scales',
                          required=True,
                          default='original')

