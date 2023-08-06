# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets import common
from plone.app.layout.viewlets import content

from plone.app.i18n.locales.browser import selector

# Sample code for a basic viewlet (In order to use it, you'll have to):
# - Un-comment the following useable piece of code (viewlet python class).
# - Rename the vielwet template file ('browser/viewlet.pt') and edit the
#   following python code accordingly.
# - Edit the class and template to make them suit your needs.
# - Make sure your viewlet is correctly registered in 'browser/configure.zcml'.
# - If you need it to appear in a specific order inside its viewlet manager,
#   edit 'profiles/default/viewlets.xml' accordingly.
# - Restart Zope.
# - If you edited any file in 'profiles/default/', reinstall your package.
# - Once you're happy with your viewlet implementation, remove any related
#   (unwanted) inline documentation  ;-p


#class LanguageSelector(selector.LanguageSelector):
#    render = ViewPageTemplateFile('templates/languageselector.pt')


#class SearchBoxViewlet(common.SearchBoxViewlet):
#    index = ViewPageTemplateFile('templates/searchbox.pt')


#class LogoViewlet(common.LogoViewlet):
#    index = ViewPageTemplateFile('templates/logo.pt')


#class DocumentActionsViewlet(content.DocumentActionsViewlet):
#    index = ViewPageTemplateFile('templates/document_actions.pt')


class FooterViewlet(common.FooterViewlet):
    index = ViewPageTemplateFile('templates/footer.pt')
