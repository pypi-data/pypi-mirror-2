#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
from zope.component import queryUtility
from zope.pluggableauth.interfaces import IPrincipalCreated
from zope.security.interfaces import IGroup, IGroupAwarePrincipal
from zope.authentication.interfaces import IAuthenticatedGroup, IEveryoneGroup


@grok.subscribe(IPrincipalCreated)
def GrantSpecialGroupsMembership(event):
    principal = event.principal
    if (IGroup.providedBy(principal) or
        not IGroupAwarePrincipal.providedBy(principal)):
        return

    everyone = queryUtility(IEveryoneGroup)
    if everyone is not None:
        principal.groups.append(everyone.id)

    auth = queryUtility(IAuthenticatedGroup)
    if auth is not None:
        principal.groups.append(auth.id)
