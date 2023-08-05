if context.meta_type == 'ATTopic':
    return True

if not context.isPrincipiaFolderish \
        and context.meta_type not in ('ATFile','ATImage'):
    return True
return False
