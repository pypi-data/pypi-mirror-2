## Script (Python) ""
##bind container=container
##bind context=context
##bind subpath=traverse_subpath
##parameters=object
##title=
##

view = object.getViewTemplateId()

return 'context/%s/macros/main' % view
