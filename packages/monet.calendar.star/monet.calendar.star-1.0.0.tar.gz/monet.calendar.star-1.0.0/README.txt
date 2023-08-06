.. contents::

Introduction
============

The *monet.calendar.star* suite is a complete event managing solution for Plone, inspired by
needs of the `City of Modena`__. Is widely used for managing all kind of events.

__ http://www.comune.modena.it/

This is only a transitional package, for downloading and installing all other products in the suite
in a simple way.

Features
========

We want to give to Plone an event type that:

* hide totally the "time" data (managed as simple text)
* give a closed (but configurable) set of type of events
* the days of weeks where really the event take place
* be able to manage special days where the event *don't* take place
* a lot of additional text information

See the `monent.calendar.event page`__ for know how to configure the event.

__ http://pypi.python.org/pypi/monet.calendar.event

Additionally one or more Plone folder can be marked as "*Calendar section*" in a new "Calendar" menu.

.. figure:: http://keul.it/images/plone/monet.calendar.suite-1.0.0-01.png
   :alt: The new Calendar menu

   Entries inside the new "Calendar menu"

This mean that this folder can use the "*Calendar view*" that show events in the current day, taken
(by default, see below) from all the site events. This search take care of counting exceptions and
days of the week of events.

.. figure:: http://keul.it/images/plone/monet.calendar.suite-1.0.0-02.png
   :alt: Single day view

   The "Calendar view"

Every event (and the also calendar sections) will also show a new "search" section at the top. This
form can be used to perform a search on events of the calendar.

.. figure:: http://keul.it/images/plone/monet.calendar.suite-1.0.0-03.png
   :alt: As new events looks like

   The search form on events

The form can be used to expand the search to more than one day, showing a summary of all events, per-day

.. figure:: http://keul.it/images/plone/monet.calendar.suite-1.0.0-04.png
   :alt: Search results on multiple days

   Search results on multiple days

Use multiple calendar: "Calendar root" sections
-----------------------------------------------

Using again the "*Calendar menu*" you can also mark folder as "Calendar root".
This is useful when using a Plone filled of subsites, where you can have a *main calendar* that
look at every event in the site, but also additional subcalendars (inside many calendar roots).

When a calendar perform searches inside a Calendar root, it will only look for events inside the
calendar root itself

.. figure:: http://keul.it/images/plone/monet.calendar.suite-1.0.0-05.png
   :alt: Search results on multiple days

   Same search above, but on a local calendar
   ("Subsite 1" there is a "Calendar root" section)

New calendar portlet
--------------------

The calendar construction is expensive, and not good to be used in a portlet of the site, where is
visibile (in the worst case, also not cached) in every page of the site.

When you install the monet.calendar.extension product, the calendar portlet is replaced with a version
that:

* not show anymore events in a specific day
* every cell is a link that perform a day-search in the nearest calendar

"Nearest calendar" mean that is you are in inside a "calendar root" section you will be moved to
the calendar of that section.

Special event types
-------------------

From ZMI (see also `monet.calendar.event`__ configuration) you can specify one or more event type
as "special". Those are then highlighted in the single day view, below the categorizations done for
the time of event.

__ http://pypi.python.org/pypi/monet.calendar.event

Example:

* Morning
* Afternoon
* Evenengin
* *YouEventType*

Plone4Artists Calendar integration
----------------------------------

The suite were originally done for working with p4a.calendar. The compatibility code is still there,
but has not been tested in latests releases. 

Dependencies tree
=================

You can freely install single components of the suite, that are:

* monet.recurring_event

  * p4a.plonecalendar (optional, see below)

  * rt.calendarinandout

    * collective.js.jqueryui

* monet.calendar.event

* monet.calendar.extensions

Requirements
============

The monet.calendar.star solution works onto:

* Plone 3.2
* Plone 3.3
* Plone 4

Under Plone 4 the integration with the "Sunburst theme" is not perfect.
See also `#11474`__.

__ http://dev.plone.org/plone/ticket/11474

Credits
=======
  
Developed with the support of `Rete Civica Mo-Net - Comune di Modena`__;
Rete Civica Mo-Net supports the `PloneGov initiative`__.

.. image:: http://www.comune.modena.it/grafica/logoComune/logoComunexweb.jpg 
   :alt: Comune di Modena - logo

__ http://www.comune.modena.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

