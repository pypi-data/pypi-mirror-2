from zope import interface, schema
from collective.collage.imagetags import message_factory as _

class IImageTagsSettings(interface.Interface):
    """ Settings for imagetags view for Collage
    """
    scale = schema.Choice(title=_(u"Image scale"),
                          vocabulary='collective.collage.imagetags.scales',
                          required=True,
                          default='image')

