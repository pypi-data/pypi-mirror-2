from Products.Five import BrowserView
from Acquisition import aq_inner

class TransformView(BrowserView):

    def transform(self):
        method = self.request.form.get('method')
        context = aq_inner(self.context)
        target = context.absolute_url() + '/view'
        if not method is None:
            context.transformImage(method)
        self.request.RESPONSE.redirect(target)
