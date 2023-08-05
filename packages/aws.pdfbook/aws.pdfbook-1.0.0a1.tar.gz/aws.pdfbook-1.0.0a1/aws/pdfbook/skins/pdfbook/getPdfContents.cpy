## Script (Python) ""
##bind container=container
##bind context=context
##bind subpath=traverse_subpath
##parameters=
##title=
##

if context.meta_type == 'ATTopic':
    objects = context.queryCatalog(batch=True,b_start=0,sort_limit=100000,b_size=1000000)
    # ifnore folderish types
    objects = [o for o in objects if not o.is_folderish \
                        and o.meta_type not in ('ATFile','ATImage')]
else:
    objects = [context]

return objects
return [o.meta_type for o in objects]
