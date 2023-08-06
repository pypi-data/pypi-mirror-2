===========
Dolmen Site
===========

:Test-Layer: functional

Dolmen is a simple application. The package `dolmen.app.site` provides
an easy way to bootstrap your own applications. It exposes two elements,
the Dolmen object and the IDolmen interface.

This creation of Dolmen Application is straightforward::

    >>> import grokcore.component as grok
    >>> from zope.event import notify
    >>> from zope.lifecycleevent import ObjectCreatedEvent
    >>> from dolmen.app.site import Dolmen, IDolmen

    >>> rocks = Dolmen()
    >>> notify(ObjectCreatedEvent(rocks))

    >>> IDolmen.providedBy(rocks)
    True

It's a valid `zope.component` ``ISite``:

    >>> import zope.component
    >>> from zope.component.interfaces import ISite, IPossibleSite
    >>> from zope.site.site import LocalSiteManager

    >>> IPossibleSite.providedBy(rocks)
    True

    >>> ISite.providedBy(rocks)
    False

    >>> site = LocalSiteManager(rocks)
    >>> rocks.setSiteManager(site)
    >>> rocks.getSiteManager()
    <LocalSiteManager ++etc++site>


Dolmen is a `dolmen.content` Container (read `dolmen.content`
documentation for more information)::

    >>> from dolmen.content import IContent, IContainer
    >>> IContent.providedBy(rocks)
    True
    >>> IContainer.providedBy(rocks)
    True
