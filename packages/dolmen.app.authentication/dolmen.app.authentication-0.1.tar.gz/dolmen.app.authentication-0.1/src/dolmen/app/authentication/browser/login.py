#!/usr/bin/python
# -*- coding: utf-8 -*-

import zope.schema
import zope.interface
import grokcore.view as grok

from zope.event import notify
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.location.interfaces import ILocation

from dolmen.app.layout import Form
from dolmen.forms.base import Fields, button
from dolmen.authentication import UserLoginEvent
from dolmen.app.authentication import MF as _
from dolmen.app.authentication.browser import AnonymousMenuEntry


class ILoginForm(zope.interface.Interface):
    """A simple login form interface.
    """
    login = zope.schema.TextLine(
        title=_(u"Username"),
        required=True)

    password = zope.schema.Password(
        title=_(u"Password"),
        required=True)


class Login(Form, AnonymousMenuEntry):
    """A very basic implementation of a login form.
    """
    grok.title(_(u"Log in"))
    grok.require('zope.Public')
    grok.context(zope.interface.Interface)

    prefix = ""
    label = _(u"Identify yourself")
    form_name = _(u"Login form")
    fields = Fields(ILoginForm)

    def updateWidgets(self):
        Form.updateWidgets(self)
        self.widgets.prefix = ''
        self.widgets.update()

    @button.buttonAndHandler(_('Log in'), name='login')
    def login(self, data):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            self.status = _(u"Login failed")
        else:
            self.flash(_('You are now logged in as ${name}',
                         mapping={"name": principal.id}))
            notify(UserLoginEvent(principal))
            camefrom = self.request.get('camefrom', None)
            if not camefrom:
                if ILocation.providedBy(principal):
                    camefrom = absoluteURL(principal, self.request)
                else:
                    camefrom = absoluteURL(self.context, self.request)
            self.redirect(camefrom)
