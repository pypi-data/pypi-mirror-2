Introduction
============

This package extends the default Plone portlets framework to allow for the assignment
of portlets on a per-view basis.


Overview
--------

Sometimes it may really be useful to have a different portlet assigned to
standalone views which are not necessary coupled to any content objects.
You may think that in this case it is possible to create a new content object
and apply that view to it and then finally assign the required portlets to
that object. However, in ``Plone`` you may end up creating new content objects
for every standalone zope3 view - which is not correct from a content management
point of view.

In one of our projects we had a lot of standalone views where it was a requirement
to have different portlets assigned to a standalone view (e.g. having a separate set of
portlets on user profile views, sitemap view, ``z3c.form`` form views, homepage view, etc.)

To facilitate the adding of portlets there we developed this package called
``collective.viewportletmanager``. It is aimed at usage by ``Plone`` integrators
and is not working out of the box. To be able to assign portlets to your zope3
view you have to follow some simple rules.

More on this below in ``How to use`` section.


Compatibility
-------------

This add-on was tested on ``Plone 3.3.5`` and ``Plone 4.1``


Installation
------------

* to add the package to your ``Zope`` instance, please, follow the instructions
  found inside the ``docs/INSTALL.txt`` file
* then restart your ``Zope`` instance
* and install the ``View Portlet Manager package from within the ``portal_quickinstaller`` tool


How to use
----------

This packages allows you to assign ``Plone 3`` portlets to your custom zope3
views. To be able to do this we require from you the only one extra step:
mark your view with ``IPortletsAwareView`` interface::

    from zope.interface import implements
    from Products.Five.browser import BrowserView
    from collective.viewportletmanager.interfaces import IPortletsAwareView
    
    class MyZope3View(BrowserView):
        implements(IPortletsAwareView)
        
        # your zope3 view code goes here

After you declare that your zope3 view implements ``IPortletsAwareView``
interface, restart your zope instance and render your view. From now on you'll
see there ``Manage view portlets`` link. This link will get you to portlets
management screen which is exactly the same as default ``Manage portlets`` view.
The only difference is that ``Manage view portlets`` view will allow you to
manage portlets for your ``IPortletsAwareView`` marked view.

The portlets you add on that view will be available only while visiting your
custom zope3 view.

One more important note here is that portlets are not assigned based on view alone,
but are based on context object as well. So we may say that view-based portlets
are actually view-context based portlets.

View portlets will go right after context based portlets like other site-wide
portlets.

You'll also be able to block view based portlets via the standard ``Manage
portlets`` screen.


Design Notes
------------

The main thing is that view portlets are saved into ``Plone`` site root
annotations like any other site-wide portlet categories but at the same time
view category mappings hold context object UIDs so actually view category
doesn't look like site-wide but context based portlets category.

View portlets category uses the next assignments key format::

    "<object_uid>:<view_name>"
    
So, for object with uid equal "123" and it's view called "my-view" we'll get
portlet assignments saved under "123:my-view" key in "view" category inside
global site portlet manager annotations.

For site root, which doesn't provide "UID" attribute we use string placeholder
"nouid". E.g. portlet assignments for "sitemap" view will be saved under
"nouid:sitemap" key.


This package overrides a bunch of standard ``Plone`` portlets framework
components in order to add view portlets category to list of standard
portlet categories: context, user, group and content type.

Here we'll try to describe what exactly was overridden:

``PortletContext`` both for site root and site content in order to add view
category to standard categories list. This context also takes care of
generating view key based on object "UID" and view name. To get view name
portlet context retrieves view as an argument to it's
``globalPortletCategories`` method, which actually breaks default ``Plone``
portlets framework designed API. To pass view object around we also had to
override portlet manager renderer and portlet retrievers.

``PortletManagerRenderer``: to pass view object down to portlet retriever class.

``PortletRetriever``: to pass view object down to ``PortletContext`` which in
turn will use it to generate view category key.

``ContextualEditPortletManagerRenderer`` view to provide view category blacklist
status to be used on standard ``Manage portlets`` screen.

``EditPortletManagerRenderer`` to disable inherited portlets on ``Manage view
portlets`` screen. This doesn't make much sense for view category portlets.

``ManageContextualPortlets`` to provide set blacklist status method which will
also take care of view category blacklist status.

``ManageViewPortlets``: our own ``Manage view portlets`` view

``ManageViewPortletsLinkViewlet``: our own viewlet that renders ``Manage view
portlets`` link pointing to appropriate portlets management screen for current
content object and zope3 view. Link appears only on ``IPortletsAwareView``
enabled zope3 views.


Live Examples
=============

* http://www.choosehelp.com/
* http://www.choosehelp.com/profile/John/


Credits
=======


Companies
---------

|martinschoel|_

* `Martin Schoel Web Productions <http://www.martinschoel.com/>`_
* `Contact us <mailto:python@martinschoel.com>`_


Authors
-------

* Vitaliy Podoba <vitaliy@martinschoel.com>


Contributors
------------


.. |martinschoel| image:: http://cache.martinschoel.com/img/logos/MS-Logo-white-200x100.png
.. _martinschoel: http://www.martinschoel.com/
