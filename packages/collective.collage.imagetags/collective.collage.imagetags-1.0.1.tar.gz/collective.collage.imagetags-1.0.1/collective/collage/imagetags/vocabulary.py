from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.Archetypes.interfaces import IBaseObject
from Products.Collage.interfaces import ICollageAlias

def ImageScalesVocabularyFactory(context):
    """
    Returns a list of all the image fields available in current object
    """
    if ICollageAlias.providedBy(context):
        try:
            context = context.get_target()
        except:
            return None
            
    if not IBaseObject.providedBy(context):
        return None

    field_scales = []
    schemata = context.Schemata()
    fieldsets = schemata.keys()
    for fieldset in fieldsets:
        for field in schemata[fieldset].fields():
            if field.getType() in ('plone.app.blob.subtypes.image.ExtensionBlobField', 'Products.Archetypes.Field.ImageField', ):
                sizes = field.getAvailableSizes(context)

                # Sorting function
                def my_sort(x,y):
                    return sizes[y][0]-sizes[x][0]

                keys = sizes.keys()
                keys.sort(my_sort)

                field_scales.append(field.getName())

                for size in keys:
                    # Remove zero sized scales
                    if sizes[size][0] > 0:
                        field_scales.append('%s_%s' % (field.getName(), size))

    
    return SimpleVocabulary.fromValues(field_scales)

directlyProvides(ImageScalesVocabularyFactory, IVocabularyFactory)
