from Products.Five import BrowserView
from Acquisition import aq_inner

from Products.CMFPlone import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

class TransformView(BrowserView):

    def transform(self):
        request = self.request
        method = request.form.get('method')
        context = aq_inner(self.context)
        error = ''
        if not method is None:
            try:
                context.transformImage(method)
            except Exception, msg:
                error = msg
                
        if 'ajax' in request.form:
            request.response.setHeader('content-type', 'text/javascript; charset=utf-8');
            if error:
                #request.response.write('{success: false, error: "%s"}' % (error))
                return '{success: false, error: {title: "%s", msg: "%s"}}' % (_(u'Error'), error)
            else:
                #request.response.write('{success: true}')
                return '{success: true}'            
        else:
            target = context.absolute_url() + '/view'
            if error:
                IStatusMessage(request).addStatusMessage(error, type='error')
                
            request.response.redirect(target)
