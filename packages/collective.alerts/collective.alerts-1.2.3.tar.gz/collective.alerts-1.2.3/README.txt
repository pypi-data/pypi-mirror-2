Introduction
============

This package implements Cory LaViska's 'JQuery Alert Dialogs' for Plone.

Basically, they are fancy, styleable replacements for the standard
'alert', 'confirm' and 'prompt' browser functions.

See http://abeautifulsite.net/blog/2008/12/jquery-alert-dialogs/ for more
details.


Usage
-----

When collective.alerts is installed and the jquery.alerts library registered in
portal_javascripts (should be automatic), then the alerts can be called as
follows:

 - jAlert( message, [title, callback] )
 - jConfirm( message, [title, callback] )
 - jPrompt( message, [value, title, callback] )


Dependencies:
-------------
On Plone 3.x, make sure that you have a newer version of JQuery than what is
shipped with Plone. That would be JQuery > 1.3.5

The easiest way to do this is to install collective.js.jquery.

Plone 4.x users already have a new enough version of JQuery.
