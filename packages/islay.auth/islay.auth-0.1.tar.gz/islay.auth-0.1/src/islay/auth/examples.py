from repoze.who.plugins.form import RedirectingFormPlugin as RFP

class RedirectingFormPlugin(object):
    def __new__(self):
        return RFP('http://plone.org/login_form', 'http://plone.org/login', 'http://plone.org/logout', 'None')
