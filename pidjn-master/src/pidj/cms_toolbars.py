from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

class MyToolbarClass(CMSToolbar):

    def populate(self):
        self.toolbar.add_link_item(     # or add_button(), add_modal_item(), etc
            name='A link',
            url='#'
        )

toolbar_pool.register(MyToolbarClass)
