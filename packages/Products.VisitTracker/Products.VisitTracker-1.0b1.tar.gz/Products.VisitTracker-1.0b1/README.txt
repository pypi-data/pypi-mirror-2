Introduction
============

Products.VisitTracker provides a simple API for tracking visits on
objects. Objects for which visits should be tracked have to implement
the::

    Products.VisitTracker.interfaces.IVisitable

interface and thus provide an attribute named *revisit* which defines
the time delta in hours after which a revisit is tracked as a new visit.

Visits are tracked by the IVisitTracker adapter and stored as annotations
on the specific object.


Usage
=====

Given an object implementing the IVisitable interface tracking and retrieving
visits is done by adapting to IVisitTracker.

::

    tracker = IVisitTracker(obj)

Tracking a visit
----------------

Tracking a visit is done by calling the *trackVisit* method. This is usually
done in a view or a viewlet.

::

    tracker.trackVisit()

Getting visits
--------------

There are multiple methods available to retrieve the stored visits.

Get visits
``````````

::

    tracker.getVisits()

Returns a list of date, userid tuples of all visits tracked for this object.

Get number of visits
````````````````````

::

    tracker.getNumberOfVisits()

Returns the number of visits tracked for this object.

Get last visit
``````````````

::

    tracker.getLastVisit()

Returns the date of the last visit tracked for this object.

Get last visit of user
``````````````````````

::

    tracker.getLastVisit(userid)

Returns the date of the last visit of the specified user tracked for this object.

Get last visits by user
```````````````````````

::

    tracker.getLastVisits()

Returns a list of userid, date tuples of the last visits of all tracked users.

