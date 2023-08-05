import grok


class CanLogin(grok.Permission):
    grok.name('dolmen.user.CanLogin')
    grok.title('dolmen: anonymous can login')


class CanLogout(grok.Permission):
    grok.name('dolmen.user.CanLogout')
    grok.title('dolmen: user can logout')


class AddUsers(grok.Permission):
    grok.name('dolmen.security.AddUsers')
    grok.title('dolmen.security: add users')


class ManageUsers(grok.Permission):
    grok.name('dolmen.security.ManageUsers')
    grok.title('dolmen.security: manage users')
