=======================
dolmen.app.viewselector
=======================

The package ``dolmen.app.viewselector`` is an extension for `Dolmen`
applications, allowing a basic management of alternative views.


About
=====

In a CMS, it's often very useful to be able to design and provide several
views for a single item. These views can be relevant, according to a given
context and situation. `dolmen.app.viewselector` allows you to define a
view as being an "alternate" option to render a given context. A menu then
provides you the machinery to select the most relevant view for your
usecase.


A quick overview
================

To know that a component can provide alternative views, we need to
explicitly specify it. An interface defines the "selector" capability::

  >>> from dolmen.app.viewselector import IViewSelector
  >>> list(IViewSelector)
  ['selected_view']

  >>> IViewSelector['selected_view']
  <...TextLine...>

The IViewSelector interface defines a single field, known as
'selected_view'. The field value is merely the name of the Page
component currently used::

  >>> IViewSelector['selected_view'].default
  u'base_view'

Out of the box, the default value is set to 'base_view'.


Defining the content
====================

To demonstrate the alternative views, we first need a context that is
aware of the views selection::

  >>> from zope.location import Location
  >>> from zope.interface import implements

  >>> class Bear(Location):
  ...  implements(IViewSelector)
  ...  selected_view = u"sleeping"

We defined the default view to the view named "sleeping".


Defining alternate views
========================

The alternative views are 'pages' (see ``megrok.layout`` and
``dolmen.app.layout``) that are registered onto a dedicated menu.
To define an alternative view, we inherit from the ``AlternativeView``
base class::

  >>> import grokcore.view as grok
  >>> from grokcore.component import testing
  >>> from dolmen.app.viewselector import AlternativeView

  >>> class Sleeping(AlternativeView):
  ...   grok.context(Bear)
  ...   grok.title("Sleeping bear")
  ...
  ...   def render(self):
  ...     return u"RRrrr..."

  >>> testing.grok_component('sleeping', Sleeping)
  True

The "sleeping" view that we defined as a default value for our IViewSelector
is now defined and registered. Let's register 2 other views, to populate
the menu and provide a "realistic" usecase::

  >>> class PolarFur(AlternativeView):
  ...   grok.context(Bear)
  ...   grok.title("Polar bear")
  ...
  ...   def render(self):
  ...     return u"I'm white !"

  >>> testing.grok_component('polar', PolarFur)
  True

  >>> class SpringFur(AlternativeView):
  ...   grok.context(Bear)
  ...   grok.title("Spring bear")
  ...   grok.require("dolmen.content.Edit")
  ...
  ...   def render(self):
  ...     return u"I'm brown !"

  >>> testing.grok_component('spring', SpringFur)
  True


Default dynamic index
=====================

In order to render the selected view, another view is used. We may call it a 
"routing" view, as it's used to lookup and render the desired component.

We first need to instance the two needed components, the content and
the request ::

  >>> from zope.publisher.browser import TestRequest

  >>> herman = Bear()
  >>> request = TestRequest()

The content provides IViewSelector, the interface for which the "routing"
view is registered::

  >>> IViewSelector.providedBy(herman)
  True

The "routing" view is by convention called "index" and can be looked up
as a basic view::

  >>> from zope.component import getMultiAdapter
  >>> index = getMultiAdapter((herman, request), name="index")
  >>> index
  <dolmen.app.viewselector.select.SelectedView...>

This view, when rendered, will look up and render the view named as the
`selected_view` attribute, registered for the same content and request::

  >>> herman.selected_view
  u'sleeping'

  >>> index.render()
  u'RRrrr...'

If we set a different value for the `selected_view` attribute, the looked up
view changes accordingly::
  
  >>> herman.selected_view = u"polarfur"
  >>> index.render()
  u"I'm white !"

  >>> herman.selected_view = u"springfur"
  >>> index.render()
  u"I'm brown !"

If the view doesn't exist, a base message is returned::

  >>> herman.selected_view = u"nothing"
  >>> index.render()
  u'The selected view is not a valid IPage component.'


Applying the view via the User interface
========================================

The selected view can be chosen from a list of available alternative view.
This choice is made via a menu, for which the views are registered.

Menu
----

Let's render the menu, to have a look at its structure.
Before we can get a functional menu, which requires a located content, we need
to persist our content in a functional site::

  >>> from zope.component.hooks import getSite
  >>> site = getSite()

  >>> herman = site['herman'] = herman
  >>> herman.__name__
  u'herman'

The content located, we can instanciate the menu. The menu is handled by
``megrok.menu`` and is a ``zope.browsermenu.IBrowserMenu`` component.

A viewlet is registered in order to render this menu is a conventional way::

  >>> baseview = Sleeping(herman, request)

  >>> from dolmen.app.layout.master import AboveBody
  >>> from dolmen.app.viewselector.select import SelectableViews

  >>> manager = AboveBody(herman, request, baseview)
  >>> menu = SelectableViews(herman, request, baseview, manager)

The alternate views do use a security declaration and therefore, we need to
login as a particular user, to test the rendering. Here, the `SpringFur`
view requires the `dolmen.content.Edit` permission.

Let's login as a used that doesn't have this permission granted::

  >>> login('zope.user')

When rendering the menu, the `SpringFur` component will, therefore,
be omitted::

  >>> menu.update()
  >>> print menu.render()
  <dl id="selectable-views" class="additional-actions">
    <dt>Content display</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
    	  <a href="http://127.0.0.1/herman/viewselector?name=sleeping"
             title="Sleeping bear">Sleeping bear</a>
     	</li>
       	<li class="entry">
    	  <a href="http://127.0.0.1/herman/viewselector?name=polarfur"
             title="Polar bear">Polar bear</a>
	</li>
      </ul>
    </dd>
  </dl>

  >>> logout()

If we now log in with a user with the right permission granted, we see
that the component is correctly included::

  >>> login('zope.mgr')
  >>> menu.update()
  >>> print menu.render()
  <dl id="selectable-views" class="additional-actions">
    <dt>Content display</dt>
    <dd>
      <ul class="menu">
        <li class="entry">
    	  <a href="http://127.0.0.1/herman/viewselector?name=sleeping"
             title="Sleeping bear">Sleeping bear</a>
     	</li>
       	<li class="entry">
    	  <a href="http://127.0.0.1/herman/viewselector?name=polarfur"
             title="Polar bear">Polar bear</a>
	</li>
    	<li class="entry">
    	  <a href="http://127.0.0.1/herman/viewselector?name=springfur"
             title="Spring bear">Spring bear</a>
    	</li>
      </ul>
    </dd>
  </dl>

  >>> logout()


Apply
-----

The menu above exposes the view 'viewselector', registered for a 
IViewSelector content. This view is the component that effectively
changes the `selected_view` attribute to the clicked value.

Let's simulate a click to test that view. The current value of the 
`selected_view` attribute is inconsistant::

  >>> herman.selected_view
  u'nothing'

We want it changed to something existing, like the `PolarFur` view::

  >>> request = TestRequest(form={'name': u'polarfur'})
  >>> handler = getMultiAdapter((herman, request), name="viewselector")
  >>> handler
  <dolmen.app.viewselector.select.ApplyView ...>

Logged in as an admin user, we can apply the selected view::

  >>> login('zope.mgr', request)
  >>> handler()
  'http://127.0.0.1/herman'

The view redirects you to the base view of the content. The value is
now changed::

  >>> herman.selected_view
  u'polarfur'
