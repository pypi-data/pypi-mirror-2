Introduction
============

A python package that simply registers the jqueryui javascript library as zope browser resources.


Why
---

I previously used collective.js.jqueryui but was frustrated with it's use and upgrade issues since
it's no longer compatible with Plone 3--this really confuses users of dependent products.

This is simple, doesn't register an install GS step and allows the user to decide how they want to use
the javascript library on the system.

Also, doing it this way will allow you to get specific versions of jqueryui since the version number
of this package will match the version number of jqueryui.


Javascript Files
----------------

* ++resource++collective.javascript.jqueryui/js/jquery-ui.min.js
* ++resource++collective.javascript.jqueryui/js/jquery-1.4.2.min.js


Available Themes
----------------

* ++resource++collective.javascript.jqueryui/css/ui-lightness/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/ui-darkness/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/sunny/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/start/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/smoothness/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/redmond/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/hot-sneaks/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/eggplant/jquery-ui.css
* ++resource++collective.javascript.jqueryui/css/blitzer/jquery-ui.css

