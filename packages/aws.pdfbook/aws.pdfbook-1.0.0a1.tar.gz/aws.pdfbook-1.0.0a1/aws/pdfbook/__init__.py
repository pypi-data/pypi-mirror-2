# -*- coding: utf-8 -*-
# $Id: __init__.py 22 2010-04-26 18:10:54Z glenfant $
"""aws.pdfbook component for Plone"""

import logging
from Products.CMFCore import utils

from config import PROJECTNAME

logger = logging.getLogger(PROJECTNAME)
from zope.i18nmessageid import MessageFactory
translate = MessageFactory(PROJECTNAME)
