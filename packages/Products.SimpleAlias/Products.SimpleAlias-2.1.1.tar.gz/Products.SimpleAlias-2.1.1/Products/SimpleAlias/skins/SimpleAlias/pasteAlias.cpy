## Controller Python Script "pasteAlias"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Paste objects as Aliases into a folder
##
# $Id: pasteAlias.cpy 123908 2010-08-20 10:27:22Z glenfant $

from ZODB.POSException import ConflictError
from Products.SimpleAlias import SimpleAliasMessageFactory as _

msg = _(u'Copy one or more items first.')

if context.cb_dataValid:
    try:
        res = context.simplealias_tool.manage_pasteAsAlias(context)

        from Products.CMFPlone.utils import transaction_note
        transaction_note('Pasted content as Alias to %s' % (context.absolute_url()))
        context.plone_utils.addPortalMessage(res)
        return state

    except ConflictError:
        raise
    except AttributeError:
        msg = _(u'Paste as Alias could not find clipboard content.')

context.plone_utils.addPortalMessage(msg)
return state.set(status='failure')
