Introduction
============

Google docs viewer is a service provided by google tm: https://docs.google.com/viewer

This add-on add a view on the File content type.  It display the file with the
embed viewer. You can find a live demo at toutpt.makina-corpus.org/add-ons/collective.googledocsviewer/cv-jeanmichel-francois-fr/view

How to use it
=============

Add a file content in your Plone site, make it publicly available (publish it) and
select the google docs 'Google Docs viewer' view in the display drop down menu.

Next you can use the the 'Configure view' action provided at the bottom of the page
to configure the size of the viewer you want to use.

How it works
============

It display an iframe built from your file's url.

For example, http://example.com/myfile/view  will become ::

  <iframe src="http://docs.google.com/viewer?url=http%3A%2F%2Fexample.com%2Fmyfile&embedded=true" width="600" height="780" style="border: none;"></iframe>

Sizes are stored on site level in plone.app.registry or on context level with annotations.
