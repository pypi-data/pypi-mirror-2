from Products.Collage.browser.viewlet import SimpleContentMenuViewlet
from Products.Collage.interfaces import IDynamicViewManager


class ImageTagsSettingsViewlet(SimpleContentMenuViewlet):
    def uses_tags_layout(self):
        manager = IDynamicViewManager(self.getImmediateObject())
        return manager.getLayout() == 'tags'
