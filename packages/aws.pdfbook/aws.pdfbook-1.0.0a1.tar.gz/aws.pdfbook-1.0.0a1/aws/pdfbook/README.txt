Description

    PDFBook is a product that adds a new style to a Plone 2.1.x portal.
    It creates a new skin selection to the 'portal_skins' tool
    (called PDFBook), and registers a custom stylesheet (called pdfbook.css)
    with the 'portal_css' tool.

    PDFBook is based on DIYPloneStyle 1.0.4, a skeleton product
    ready for building new graphical designs for Plone.

Installation

    Place PDFBook in the Products directory of your Zope instance
    and restart the server.

    In Plone go to the 'Site Setup' page and click on the 'Add/Remove
    Products' link.

    Choose PDFBook (check its checkbox) and click the 'Install' button.

    You may have to empty your browser cache to see the effects of the
    product installation/uninstallation.

    Uninstall -- This can be done from the same management screen.

Selecting a skin

   Depending on the value given to SELECTSKIN (in config.py), the skin will be
   selected (or not) as default one while installing the product. If you need
   to switch from a default skin to another, go to the 'Site Setup' page, and
   choose 'Skins' (as portal manager). You can also decide from that page if
   members can choose their preferred skin and, in that case, if the skin
   cookie should be persistent.

   Note -- Don't forget to perform a full refresh of the page or reload all
   images (not from browser cache) after selecting a skin.
   In Firefox, you can do so by pressing the 'shift' key while reloading the
   page. In IE, use the key combination <Ctrl-F5>.

Written by

    John Doe <john.doe@dev.null>
