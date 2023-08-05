from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.Archetypes.interfaces import IBaseObject
from Products.Collage.interfaces import ICollageAlias

def ImageFieldsVocabularyFactory(context):
    """
    Returns a list of all the image fields available in current object
    """
    if ICollageAlias.providedBy(context):
        try:
            context = context.get_target()
        except:
            return None
            
    items = []
    images = []
    if not IBaseObject.providedBy(context):
        return None

    image_fields = []
    schemata = context.Schemata()
    fieldsets = schemata.keys()
    for fieldset in fieldsets:
        for field in schemata[fieldset].fields():
            if field.getType() in ('plone.app.blob.subtypes.image.ExtensionBlobField', 'Products.Archetypes.Field.ImageField', ):
                image_fields.append(field)
                
    for field in image_fields:
        items.append(field.getName())
    
    return SimpleVocabulary.fromValues(items)

directlyProvides(ImageFieldsVocabularyFactory, IVocabularyFactory)

def ImageScalesVocabularyFactory(context):
    """Vocabulary factory with the typical image scales.
       TODO: Dynamically calculate image scales of all images in object
    """
    values = ('original', 'large', 'preview', 'mini', 'thumb', 'tile', 'icon', 'listing',)            
    return SimpleVocabulary.fromValues(values)

directlyProvides(ImageScalesVocabularyFactory, IVocabularyFactory)
