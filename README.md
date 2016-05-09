[![Build Status](https://travis-ci.org/ccnmtl/django-pagetimer.svg?branch=master)](https://travis-ci.org/ccnmtl/django-pagetimer)
[![Coverage Status](https://coveralls.io/repos/github/ccnmtl/django-pagetimer/badge.svg?branch=master)](https://coveralls.io/github/c
cnmtl/django-pagetimer?branch=master)

# django-pagetimer

Simple but effective endpoint for tracking users' time spent on pages.

## background

Often, we have clients ask to see metrics on how long users spent on
each page of the application. Tracking that *properly* in the wild is
actually really difficult and comes with a lot of caveats (eg, we can
tell if they have the browser open to the page, but not that someone
is actually looking at it; they may have wandered off with the tab
open).

This library provides a django app that implements a simple, but
surprisingly effective approach to solving that problem in the general
case.

At its core, there's a templatetag that inserts a bit of JS (with no
dependencies) that just does a heartbeat back to an endpoint once
every 60s (configurable). The backend endpoint stores an entry with
username, session id, ipaddress, path, and a timestamp. From there,
reports can be generated and timelines reconstructed with a reasonable
accuracy (commensurate with the amount of effort required to
implement).

Much more accurate and complex approaches can be taken, but in my
experience, this is good enough to drop in quickly and get started. It
creates one DB entry per user per minute by default, which is unlikely
to blow up your database usage too quickly. The approach encourages
you to just pull down CSVs for offline processing. Once you've been
using something like this for a while, you may have a better idea of
where you need more precision in your tracking, but this will help you
get there.

## installation

```
$ pip install django-pagetimer
```

Then add `pagetimer` to your `INSTALLED_APPS` and include
`('pagetimer/', include('pagetimer.urls'))`, in you `urls.py`.

Next, in your `base.html`, include `{% load pagetimertags %}` and,
preferably near the end of the `<head>`, insert a `{% pagetimer %}`.

Now, anytime a user is on any page of your site, their browser will
ping the pagetimer endpoint once every 60s and it will log it.

## coming soon

* admin view for downloading CSV dumps
* admin view for downloading *anonymized* CSV dumps (with username,
ipaddress anonymized)
* basic admin dashboard of recent visits
* admin function for clearing out older entries (to free up disk space
in the DB)
* pluggable backend architecture. The existing DB model will be one
  (and probably the default) model. A simple textfile appending
  backend will be added and there will be a nice interface for
  implementing, eg, an ElasticSearch backend.
