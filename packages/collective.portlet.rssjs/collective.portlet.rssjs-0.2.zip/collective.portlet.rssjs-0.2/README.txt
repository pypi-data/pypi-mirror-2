Introduction
============

Motivation
----------

Using the standard **RSS Feed** Portlet of Plone,
you may end up in blocked Zope threads when the
requested URLs are not responding in a sensible time.
This alternative prohibits this by doing 
the work on the client.

Abstract
--------

**collective.portlet.rssjs** adds a new Portlet
**RSS Feed (JS)** to the Plone Site.

This portlet uses the **GOOGLE FEEDS API**
via ajax to get and parse rss feeds.

As a boilerplate

    http://plugins.jquery.com/project/jgfeed

was used.

The dom is manipulated on the client to add the 
Feed Items.

The portlet has the same markup as the std Plone 
**RSS Feed** portlet.
