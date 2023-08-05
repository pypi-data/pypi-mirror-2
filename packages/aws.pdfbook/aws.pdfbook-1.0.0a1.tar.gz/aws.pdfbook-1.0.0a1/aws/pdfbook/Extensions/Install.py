from cStringIO import StringIO

from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName

from aws.pdfbook.Extensions.utils import *
from aws.pdfbook.config import *

def install(self):
    out = StringIO()

    install_subskin(self, out, GLOBALS)
    registerStylesheets(self, out, STYLESHEETS)
    registerScripts(self, out, JAVASCRIPTS)

    portal = getToolByName(self,'portal_url').getPortalObject()

    if 'portal_pdf' not in portal.objectIds():
        addTool = portal.manage_addProduct['PDFBook'].manage_addTool
        addTool('PDF Tool', None)

    at = getToolByName(self, 'portal_actions')
    try:
        at.addAction('pdf',
                     'PDF',
                     'string:$object_url/upload_pdf',
                     'object/availablePdf',
                     'View',
                     'document_actions')
    except:
        pass
    ai = getToolByName( self, 'portal_actionicons')
    try:
        ai.addActionIcon('plone', 'pdf', 'pdf_icon.gif', 'PDF')
    except:
        pass

    print >> out, "Installation completed."
    return out.getvalue()

