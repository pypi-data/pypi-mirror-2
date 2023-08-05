# -*- coding: utf-8 -*-
# $Id: pdf.py 22 2010-04-26 18:10:54Z glenfant $
"""PDF conversion tool"""

from cStringIO import StringIO
import HTMLParser
import os
import popen2
import logging
import tempfile
import shutil
import types

from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from aws.pdfbook import logger
from aws.pdfbook.config import (
    RECODE_BIN, HTMLDOC_BIN, SITE_CHARSET, DOWNLOAD_BUFFER_SIZE)


if not os.path.isfile(RECODE_BIN):
    HAS_RECODE = False
    logger.info("'%s' binary not found", RECODE_BIN)
else:
    HAS_RECODE = True

if not os.path.isfile(HTMLDOC_BIN):
    HAS_HTMLDOC = False
    logger.info("'%s' binary not found", HTMLDOC_BIN)
else:
    HAS_HTMLDOC = True

CHAR_MAPPING = {
    u"'": unichr(226) + unichr(128) + unichr(153),
    }


def recode(data):
    """Use recode binary to fix encoding problems
    """
    if HAS_RECODE:
        recodeout, recodein = popen2.popen2("%s %s..html-i18n" %
                                            (RECODE_BIN, SITE_CHARSET))
        recodein.write(data)
        recodein.close()
        data = recodeout.read()
        recodeout.close()
        return data
    else:
        logger.error("Can't use recode for %s", data)
        return ''


class RecodeParser(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.data = StringIO()
        self.images = []

    def image_feed(self, tag, attrs):
        """Handle image
        """
        for k, v in attrs:
            if k == 'src':
                self.images.append(v)
                path = os.path.basename(v)
                break
        self.data.write(u'<img src="%s" />' % path)

    def handle_comment(self, data):
        self.data.write('<!-- %s -->' % data)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.image_feed(tag, attrs)
            return
        self.handle_data(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            self.image_feed(tag, attrs)
            return
        self.data.write('<%s />' % (tag,))

    def handle_endtag(self, tag):
        self.data.write('</%s>' % tag)

    def handle_data(self, data):
        """Text handling
        recode data from site charset to iso
        @param data:unicode raw text
        """

        try:
            data = data.encode('iso-8859-15', 'strict')
        except UnicodeError, e:
            data = data.encode('utf-8', 'ignore')
            data = recode(data)
        self.data.write(data)

    def recode_data(self, data):
        for k, v in CHAR_MAPPING.items():
            data = data.replace(v, k)
        self.feed(data)
        return self.data.getvalue()

    def save_images(self, portal, context, tmp_dir):
        """Save images from ZODB to temp directory
        """
        portal_url = portal.absolute_url()
        if not portal_url.endswith('/'):
            portal_url += '/'
        portal_path = '/'.join(portal.getPhysicalPath())
        object_path = '/'.join(context.getPhysicalPath())

        reference_tool = getToolByName(portal, 'reference_catalog')
        for image in self.images:
            path = image.replace(portal_url, '')
            filename = os.path.basename(path)

            object = None
            # using uid
            if image.find('resolveuid') != -1:
                uuid = image.split('/')[-1]
                object = reference_tool.lookupObject(uuid)
                logger.debug("Get image from uid %s", uuid)

            if not object:
                # relative url
                try:
                    object = context.restrictedTraverse(image)
                    logger.debug("Get image from context")
                except:
                    logger.debug("Failed to get image from context path %s",
                                 image)
            if not object:
                # absolute url
                image_path = '/'.join((portal_path, path))
                try:
                    object = portal.restrictedTraverse(image)
                    logger.debug("Get image from portal")
                except:
                    logger.debug("Failed to get image from portal path %s",
                                 image_path)
                    continue
            data = ''
            if object.meta_type == 'Portal Image':
                data = object.data
            elif object.meta_type == 'ATImage':
                data = object.getImage()
                data = getattr(object,'data', data)
            if data:
                image_file = open(os.path.join(tmp_dir, filename) , 'w')
                image_file.write(str(data))
                image_file.close()


class PDFObject(object):
    """Adapter on content item
    """
    def __init__(self, context):
        self.context = context
        self.context.REQUEST.form['is_pdf'] = True
        self.portal = getToolByName(self.context,'portal_url').getPortalObject()

    def get_html(self):
        """Return core html of the object
        """
        html = None
        if self.context.meta_type != 'ATTopic':
            template = '%s_pdf' % (self.context.meta_type.replace(' ','_').lower(),)
            html = getattr(self.context, template, None)
        if not callable(html):
            template = 'pdf_template'
            html = getattr(self.context, template, None)
        if callable(html):
            logger.debug("Got html callable %s for %s",
                         template, self.context.getId())
            html = html()
            return html
        else:
            logger.error("No callable method found to render %s",
                         self.context.getId())
            return ''

    def upload_pdf(self):
        """Upload a pdf file
        """
        tmp_dir = tempfile.mkdtemp()
        html_filename = os.path.join(tmp_dir, self.context.getId() + '.html')
        pdf_filename = '%s-%s-%s.pdf' % (self.context.aq_parent.getId(),
                                         self.context.getId(),
                                         DateTime().strftime('%Y_%m_%d-%Hh%M'))
        pdf_filepath = os.path.join(tmp_dir, pdf_filename)
        html = self.get_html()

        if not html:
            raise ValueError, 'Failed to get html contents'

        parser = RecodeParser()
        html = parser.recode_data(html)
        parser.save_images(self.portal, self.context, tmp_dir)

        # Saving the HTML
        html_file = open(html_filename,'w')
        html_file.write(html)
        html_file.close()

        # Building the PDF
        html_doc_options = (
            '--charset iso-8859-15 '
            '--headfootsize 8.0 '
            '--bodyfont helvetica '
            '--headfootfont Helvetica-Oblique '
            '--size a4 '
            '--webpage -t pdf')
        if not HAS_HTMLDOC:
            logger.error("htmldoc not found at %s" % HTMLDOC_BIN)
            shutil.rmtree(tmp_dir)
            return html

        cmd = 'cd %s && %s %s %s > %s' % (
            tmp_dir,
            HTMLDOC_BIN,
            html_doc_options,
            html_filename,
            pdf_filepath
            )
        logger.info(cmd)
        os.system(cmd)
        return
        # Making the response and returning the PDF
        response = self.context.REQUEST.RESPONSE
        setHeader = response.setHeader
        setHeader('Content-type', 'application/pdf')
        setHeader('Content-length', str(os.stat(pdf_filepath)[6]))
        setHeader('Content-disposition',
                  'attachment; filename=%s' % pdf_filename)

        fp = open(pdf_filepath, 'rb')
        while True:
            data = fp.read(DOWNLOAD_BUFFRER_SIZE)
            if data:
                response.write(data)
            else:
                break
        fp.close()
        shutil.rmtree(tmp_dir)
        return

def publishPDFFile(context, request, options):
    html_engine = getMultiAdapter((self.context, self.request), name=u'printlayout')
    html = html_engine(context=self.context, request=self.request)

