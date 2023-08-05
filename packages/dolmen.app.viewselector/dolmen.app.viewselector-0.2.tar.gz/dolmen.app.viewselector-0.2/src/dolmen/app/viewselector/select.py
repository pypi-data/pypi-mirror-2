# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
from grokcore import message
from megrok.layout import IPage
from dolmen.app.layout import Page, MenuViewlet, master
from zope.schema import TextLine
from zope.interface import Interface
from zope.component import queryMultiAdapter


class IViewSelector(Interface):
    """A component aware of dynamic views.
    """
    selected_view = TextLine(
        title=u"View",
        default=u"base_view",
        required=True,
        )


class SelectedView(Page):
    grok.name("index")
    grok.context(IViewSelector)
    grok.require("dolmen.content.View")

    def render(self):
        rendering = queryMultiAdapter(
            (self.context, self.request), name=self.context.selected_view)
        if rendering is not None and IPage.providedBy(rendering):
            rendering.update()
            return rendering.content()
        return u"The selected view is not a valid IPage component."


class ApplyView(grok.View):
    grok.name('viewselector')
    grok.context(IViewSelector)
    grok.require("dolmen.content.Edit")

    def render(self, name=None):
        if not name or name == 'index':
            message.send(
                u"This element can't be selected as the default view.")
        else:
            self.context.selected_view = name
            message.send(
                u"%r has been selected as the default view." % name)
        return self.redirect(self.url(self.context))


class SelectableViews(MenuViewlet):
    grok.order(80)
    grok.context(IViewSelector)
    grok.viewletmanager(master.AboveBody)
    grok.require("dolmen.content.Edit")

    menu_name = u"selectable-views"
    menu_class = u"additional-actions"

    def update(self):
        self.title, actions = self.get_actions(self.context)

        if actions:
            url = self.view.url(self.context, name='viewselector')
            selected = self.context.selected_view
            self.actions = [{'url': "%s?name=%s" % (url, action['action']),
                             'title': action['title'],
                             'selected': action['action'] == selected,
                             'css': (action['action'] == selected
                                     and self.entry_class + ' selected'
                                     or self.entry_class)}
                            for action in actions]
