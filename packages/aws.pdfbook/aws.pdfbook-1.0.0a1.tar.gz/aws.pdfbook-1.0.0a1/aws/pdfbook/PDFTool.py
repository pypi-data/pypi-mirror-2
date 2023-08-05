# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from Globals import InitializeClass
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFCore.utils import (UniqueObject, SimpleItemWithProperties,
                                    getToolByName)
from aws.pdfbook.config import *
from OFS.SimpleItem import SimpleItem

from pdf import PDFObject

class PDFTool(UniqueObject, SimpleItemWithProperties):

    id = 'portal_pdf'
    meta_type = 'PDF Tool'
    icon = 'pdf_icon.gif'
    plone_tool = 1

    security = ClassSecurityInfo()

    manage_options = SimpleItemWithProperties.manage_options


    def __init__(self):
        """
        Initialize properties
        """
        self._properties = ( {'id': 'title', 'type': 'string', 'mode': 'w'},
                             {'id': 'disalow_types', 'type': 'lines', 'mode': 'w'},
                           )
        self.title = 'PDF Tool'
        self.disalow_types = []

    def upload_pdf(self, obj=None, path=None):
        """Wrapper for pdf.PDFObject
        """
        if not obj:
            obj = self.restrictedTraverse(path)

        if not obj and path:
            raise KeyError, 'No object found at %s' % path

        adapted = PDFObject(obj)
        return adapted.upload_pdf()

InitializeClass(PDFTool)
