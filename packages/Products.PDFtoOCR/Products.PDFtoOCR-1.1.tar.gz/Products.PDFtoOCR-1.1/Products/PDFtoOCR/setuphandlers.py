from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.PDFtoOCR.interfaces import IIndex
from Products.PDFtoOCR.index import Index

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('Products.PDFtoOCR_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()
    sm = portal.getSiteManager()

    if not sm.queryUtility(IIndex, name='pdf_to_ocr_indexer'):
        sm.registerUtility(Index(),
                           IIndex,
                           'pdf_to_ocr_indexer')

