Introduction
============
This product cleans up the HTML formatting problems that are introduced by pasting content from MSWord 
into Plone's RichText fields.

Every time an object is created or edited, the HTML in its RichText fields will
be sanitized.

The HTML sanitizing feature is turned on by default for all Archetype objects, but can be
turned off on a per object basis by checking a box in the 'settings' fieldset
of the default edit view.

Implementation:
---------------
This product provides an event subscriber for all BaseContent Archetypes objects that will
clean up the HTML of all the RichText fields for each object.

The cleaning and sanitizing of the HTML code is mainly done by using the lxml library:
http://codespeak.net/lxml/lxmlhtml.html by means of the htmllaundry package,
written by Wichert Akkerman.

Installation:
-------------

This Product does not have to be installed via quick_installer or the plone
control panel.

Just add it to your buildout or install via easy_install.


