from zope.component import getUtility 
from plone.app.controlpanel.form import ControlPanelView

from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _

from Products.PDFtoOCR.interfaces import IIndex

class DoIndexView(ControlPanelView):
    """Just some testing / trying out.
    """

    def index(self):
        util = getUtility(IIndex ,'pdf_to_ocr_indexer')
        util.doIndex()

        self.request.response.redirect("%s/@@pdf_ocr_status" % self.context.portal_url())

    def reindex(self):
        util = getUtility(IIndex ,'pdf_to_ocr_indexer')
        util.doReindex()

        self.request.response.redirect("%s/@@pdf_ocr_status" % self.context.portal_url())


    def reinit(self):
        util = getUtility(IIndex ,'pdf_to_ocr_indexer')
        util.reinit()
        return 'Queue is reset!'

    def getUIDInfo(self, uid):
        context = aq_inner(self.context)
        results = context.uid_catalog(UID=uid)
        doc = dict()
        if results:
            item = results[0]
            doc['Title'] = item.Title
            doc['Description'] = item.Description()
            doc['id'] = item.id
            doc['url'] = item.getObject().absolute_url()
        return doc 

    def queueStatus(self):
        util = getUtility(IIndex ,'pdf_to_ocr_indexer')
        files = util._fileList
        return  [self.getUIDInfo(f) for f in files]

    def historyStatus(self):
        util = getUtility(IIndex ,'pdf_to_ocr_indexer')
        files = util._history
        return  [self.getUIDInfo(f) for f in files]




