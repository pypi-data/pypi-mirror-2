# -*- coding: utf-8 -*-

import grok
from zope import schema
from zope.interface import Interface
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.settings import Allow
from zope.site.hooks import getSite

from dolmen.app import layout
from dolmen.app.authentication import IPrincipal
from dolmen.app.authentication import permissions
from dolmen.app.authentication import MF as _
from dolmen.forms.base import Fields


class IPrincipalRoles(Interface):
    """Defines a component allowing you to chose roles.
    """
    roles = schema.List(
        value_type=schema.Choice(vocabulary='Role Ids'),
        required=True)


class PrincipalRoles(grok.Adapter):
    """Grant a role to a principal.
    """
    grok.context(IPrincipal)
    grok.implements(IPrincipalRoles)

    def __init__(self, context):
        site = getSite()
        self.userid = context.id
        self.manager = IPrincipalRoleManager(site)

    @apply
    def roles():
        """Writable property for roles.
        """
        def get(self):
            setting = self.manager.getRolesForPrincipal(self.userid)
            return [role[0] for role in setting if role[1] is Allow]

        def set(self, roles):
            # removing undefined roles
            setting = self.manager.getRolesForPrincipal(self.userid)
            for role in setting:
                if role[0] not in roles and role[1] is Allow:
                    self.manager.unsetRoleForPrincipal(role[0], self.userid)

            # setting new roles
            for role in roles:
                self.manager.assignRoleToPrincipal(role, self.userid)

        return property(get, set)


class EditPrincipalRoles(layout.Edit):
    grok.context(IPrincipal)
    grok.name('grant_roles')
    grok.title(_(u"Grant roles"))
    grok.require(permissions.ManageUsers)

    form_name = _(u"Select the principal's roles")
    fields = Fields(IPrincipalRoles)
