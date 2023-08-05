from plone.memoize.instance import memoize
from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.publisher.browser.menu import BrowserSubMenuItem
from Products.ATContentTypes.interface import IATImage

from collective.atimage.transformmenu.interfaces import ITransformSubMenuItem, ITransformMenu, ITransformMenuLayer
from Products.ATContentTypes import ATCTMessageFactory as _

class TransformSubMenuItem(BrowserSubMenuItem):
    implements(ITransformSubMenuItem)

    title = _(u'label_transform', default=u'Transform')
    submenuId = 'plone_contentmenu_transform'

    order = 50
    extra = {'id': 'plone-contentmenu-transform'}

    def __init__(self, context, request):
        BrowserSubMenuItem.__init__(self, context, request)
        self.context_state = getMultiAdapter((context, request), name='plone_context_state')

    @property
    def action(self):
        if not IATImage.providedBy(self.context):
            return None
        else:
            return self.context.absolute_url() + '/atct_image_transform'

    @memoize
    def available(self):
        if not IATImage.providedBy(self.context) or not ITransformMenuLayer.providedBy(self.request):
            return False
        elif not self.context.hasPIL():
            return False
        else:
            return len(self.context.getTransformMap())

    def selected(self):
        return False

class TransformMenu(BrowserMenu):
    implements(ITransformMenu)

    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        transformations = context.getTransformMap()
        if not transformations:
            return results

        context_url = context.absolute_url()

        for transform in transformations:
            tvalue = transform['value']
            tid = 'transform-object_button-%s' % tvalue

            results.append({ 'title'       : _(transform['name']),
                             'description' : '',
                             'action'      : '%s/@@transform?method:int=%s' % (context_url, tvalue),
                             'selected'    : False,
                             'extra'       : {'id': tid, 'separator': None},
                             'submenu'     : None,
                             'icon'        : ''
                             })

        return results
