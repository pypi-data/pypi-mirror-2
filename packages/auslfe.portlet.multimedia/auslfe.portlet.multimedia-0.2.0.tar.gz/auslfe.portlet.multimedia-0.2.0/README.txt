Documentation
=============

Yet another multimedia/dynamic portlet for Plone that display images.

Why you can like this instead of other? Because it works with Javascript disabled (with an eye
onto the `Italian Accessibility Act`__) and is tested to work behind reverse-proxy (like
`Varnish`__).

__ http://www.pubbliaccesso.it/normative/DM080705-A-en.htm
__ http://varnish-cache.org/

How to use
----------

The main information you must provide to the portlet is a Plone collection. The collection is
used to retrieve all image-like contents from it. You can freely configure the collection to
return also other content, but only ones marked as "image-able" are used (technically speaking:
it also filter only contents that provides *IImageContent*, like "Image" and "News Item" content
type already do).

From the target collection is also used the "*Number of items*" field, to show in the portlet only
a limited number of images.

The "*Limit Search Results*" field is not directly used by this portlet, but change the collection
behaviour. Enabling the client random feature with this check selected will only reorder a limited
set of images.

Performance
-----------

What scare us about other Javascript-live multimedia portlet (besides accessibility) is the massive
use of AJAX call to the server. This can lead to two problems:

* too many request (and low performance)
* random feature could work badly with cache in front of Plone

For this reason this portlet will not query every *xyz* seconds the server, but simply get from
the server all the images, the randomly reload it client side.

The *auto-reload feature* can be disabled if you don't like it. You still have a random image
set at page load time.

Be aware: CSS styles
--------------------

Default Plone columns are narrow. Installing this will make your portlet min width a little bigger,
enough for host 2 images for every row.

TODO
====

* Tests on Plone 4: there is the new SunBurst Theme and jQuery 1.4.

Credits
=======

Developed with the support of `Azienda USL Ferrara`__; Azienda USL Ferrara supports the
`PloneGov initiative`__.

.. image:: http://www.ausl.fe.it/logo_ausl.gif
   :alt: Azienda USL's logo

__ http://www.ausl.fe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

