# -*- coding: utf-8 -*-

import grokcore.component as grok
from zope.pluggableauth.factories import PrincipalInfo
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.principalregistry.principalregistry import principalRegistry


class GlobalRegistryAuth(grok.GlobalUtility):
    """An authenticator plugin, that authenticates principals against
    the global principal registry.

    This authenticator does not support own prefixes, because the
    prefix of its principals is already defined in another place
    (site.zcml). Therefore we get and give back IDs as they are.
    """
    grok.name("globalregistry")
    grok.implements(IAuthenticatorPlugin)

    __parent__ = None

    def authenticateCredentials(self, credentials):
        """Return principal info if credentials can be authenticated
        """
        if not isinstance(credentials, dict):
            return None
        if not ('login' in credentials and 'password' in credentials):
            return None
        principal = None
        login, password = credentials['login'], credentials['password']
        try:
            principal = principalRegistry.getPrincipalByLogin(login)
        except KeyError:
            return
        if principal and principal.validate(password):
            return PrincipalInfo(unicode(principal.id),
                                 principal.getLogin(),
                                 principal.title,
                                 principal.description)
        return

    def principalInfo(self, id):
        principal = principalRegistry.getPrincipal(id)
        if principal is not None:
            return PrincipalInfo(unicode(principal.id),
                                 principal.getLogin(),
                                 principal.title,
                                 principal.description)
