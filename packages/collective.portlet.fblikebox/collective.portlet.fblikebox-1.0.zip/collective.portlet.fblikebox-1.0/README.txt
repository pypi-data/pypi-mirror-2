Introduction
============

Advertise your organization's desire to be liked with a Facebook "Like Box"
in a portlet. For more information on FB Libe Boxes, see 
http://developers.facebook.com/docs/reference/plugins/like-box .

Like boxes are implemented in IFrames, and require specification of pixel 
width and height. These are among the portlet's configurable properties.

Other configurable properties include the header, profile stream and 
connection count.

Installation
============

Simply add collective.portelet.fblikebox to your egg list. Run buildout,
restart Plone, then use the add/remove add-on configlet in site setup to
enable the add on for a particular site.

Compatability
=============

This should work with Plone 3 or 4 -- until Facebook changes the API and 
breaks it.