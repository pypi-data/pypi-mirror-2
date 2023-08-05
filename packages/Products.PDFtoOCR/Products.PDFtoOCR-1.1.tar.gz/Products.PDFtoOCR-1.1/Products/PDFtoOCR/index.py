import logging
import os
import tempfile

from zope.component import getUtility 
from persistent import Persistent
from persistent.list import PersistentList

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from OFS.SimpleItem import SimpleItem

logger = logging.getLogger('Products.PDFtoOCR')


class Index(Persistent, SimpleItem):
    """ An utility that handles (re)indexing of pdf files. A processing queue
    for indexing documents is stored here. Also a short history of recently
    indexed files is stored.
    """ 

    def __init__(self):
        self._fileList = set()
        self._history = PersistentList()

    def reinit(self):
        self.__init__()

    def _changes(self):
        self._p_changed = 1 # for persistence..    
 
    def addFile(self, uid):
        self._fileList.add(uid)
        self._changes()

    def updateHistory(self, uid):
        self._history.append(uid)
        if len(self._history) > 10:
            self._history = self._history[:10]

    def doIndex(self):
        """ Index the PDF documents in the filelist queue
        """
        filesDone = set()
        fileList = self._fileList
        portal = getUtility(ISiteRoot)

        logger.info('Start OCR indexing of pdf documents')
        logger.info('Got %s docs in file list' % len(fileList))

        # Proces pdf files for indexing
        # remove all other files
        for uid in fileList: 
            results = portal.uid_catalog(UID=uid)

            if results:
                file = results[0].getObject()
                if file.getContentType() == 'application/pdf':
                   self.ocrIndexPDF(file)
            filesDone.add(uid)

        # Remove all non-pdf documents
        self._fileList = self._fileList - filesDone
        self._changes() 
        logger.info('OCR indexing of pdf documents done')


    def doReindex(self):
        """ Indexes all pdf files
        Warning: this can take a while when you have many pdf docs
        """
        logger.info('Start OCR reindexing of pdf documents')
        portal = getUtility(ISiteRoot)
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog(Type='File')
        logger.info('Got %s docs in file list' % len(results))

        for brain in results:
            document = brain.getObject()
            if document.getContentType() == 'application/pdf':
                self.ocrIndexPDF(document)
        
        logger.info('OCR reindexing of pdf documents done')

    def ocrIndexPDF(self, document):
        """ Does OCR indexing on pdf documents
        """
        gs = os.environ.get('GS', '/usr/bin/gs')
        tess = os.environ.get('TESSERACT', '/usr/local/bin/tesseract')

        logger.info('OCR processing %s' % document.getId())

        dir1 = tempfile.mkdtemp()
        pdffilename = dir1 + '/document.pdf'
        imagefilename = dir1 + '/image_%04d.tif'
        txtfilename = dir1 + '/output'
        txtoutput = ""

        # write pdf to filesystem
        fileData = str(document.getFile().data)
        file = open(pdffilename, "wb")
        file.write(fileData)
        file.close()

        # If the text is extractable with pdftotext don't
        # do ocr processing.
        # TODO: check somewhere in Plone if the pdftotext is already done..
        pdftotext = os.popen2('pdftotext -enc UTF-8 %s -' % pdffilename)
        pdftext = pdftotext[1].read()
        if pdftext.strip():
            return None

        gsParams = [gs,
                    '-dSAFER',
                    '-dBATCH',
                    '-dNOPAUSE',
                    '-sDEVICE=tiffgray',
                    '-r250',
                    '-dTextAlphaBits=4',
                    '-dGraphicsAlphaBits=4',
                    '-dMaxStripSize=8192',
                    '-sOutputFile=%s' % imagefilename,
                    pdffilename,
                    ]

        # Convert pdf to tiff images, each page is one tiff file
        os.spawnv(os.P_WAIT, gs, gsParams)
        os.remove(pdffilename)

        dirContents = os.listdir(dir1)
        dirContents.sort()

        # tesseract has other language abbrevations and a limited amount of
        # supported languages
        language = document.Language()
        if language:
            tesseractLangs = {'de': 'deu',
                              'en': 'eng',
                              'fr': 'fra',
                              'it': 'ita',
                              'nl': 'nld',
                              'po': 'por'}
            language = tesseractLangs.get(language, 'eng')

        for image in dirContents:
            if image.startswith('image'):
                imagefilename = '%s/%s' % (dir1 , image)

                tessParams = [tess,
                              imagefilename,
                              txtfilename]
                if language:
                    tessParams.append('-l')
                    tessParams.append(language)

                # Do the OCR processing
                os.spawnv(os.P_WAIT, tess, tessParams)

                file = open(txtfilename + '.txt', "r")
                txtoutput += file.read()
                file.close()

                os.remove(txtfilename + '.txt')
                os.remove(imagefilename)

        # Clean-up temp dir
        os.rmdir(dir1)

        if txtoutput:
            document.textFromOcr = txtoutput
            document.reindexObject() 
            self.updateHistory(document.UID())

