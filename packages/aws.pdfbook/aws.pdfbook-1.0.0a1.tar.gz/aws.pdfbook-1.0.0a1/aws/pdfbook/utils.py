# -*- coding: utf-8 -*-
# $Id: utils.py 22 2010-04-26 18:10:54Z glenfant $
"""Misc utilities"""

from Products.Five.browser import BrowserView
from interfaces import IPDFTransformer
from zope.component import queryMultiAdapter
from zope.publisher.interfaces.browser import IBrowserView
from zope.app.component.hooks import getSite
from aws.pdfbook.interfaces import IPDFOptions

class PDFBookEnabled(BrowserView):

    def __call__(self):

        transformer = queryMultiAdapter((self.context, self.request), name=u'printlayout')
        portal = getSite()
        options = IPDFOptions(portal)
        return bool(transformer) and (self.context.portal_type not in options.disallowed_types)
