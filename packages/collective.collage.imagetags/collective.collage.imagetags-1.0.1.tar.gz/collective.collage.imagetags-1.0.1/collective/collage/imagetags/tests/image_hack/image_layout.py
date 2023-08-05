from Acquisition import aq_inner
from Products.Collage.browser.views import BaseView

class ImageHackView(BaseView):
    title = u"00 - Image hack"
    
    def tag(self):
        context = aq_inner(self.context)
        return context.getImage().tag()
