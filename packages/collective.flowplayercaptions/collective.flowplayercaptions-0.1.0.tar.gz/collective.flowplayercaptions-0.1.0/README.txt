.. contents:: **Table of contents**

Introduction
============

Add to Plone and `collective.flowplayer`__ captioning support through the inclusion of
`Flowplayer Captions plugin`__.

__ http://pypi.python.org/pypi/collective.flowplayer
__ http://flowplayer.org/plugins/flash/captions.html

How it works
============

After the installation of the product you'll continue the creation new video contents normally,
using the basic collective.flowplayer features.

But when you have created a new internal video content (uploading a new File inside Plone with
a compatible video format like *.flv*) then going back to edit the new video, you will find a
new *fieldset* named "*Subtitles*".

.. image:: http://keul.it/images/plone/collective.flowplayercaptions-0.1.0-01.png
   :alt: The new fieldset

If you provide "*Captions file*" in a compatible format (like *.srt*) your video will display
captions

.. image:: http://keul.it/images/plone/collective.flowplayercaptions-0.1.0-02.png
   :alt: Amazing captions!

Configuration
-------------

The captions pluging offer a great set of configuration options that you can easily change,
thanks to the collective.flowplayer structure.

You will find many new entry in the *flowplayer_properties*, but you can add new ones. Please,
see the "*Configuration*" section of the "*Flash plugin: Captions*" given above, but also the
`Display properties`__ and `Styling properties`__ of Flowplayer plugings guide.

__ http://flowplayer.org/documentation/configuration/plugins.html#display-properties
__ http://flowplayer.org/documentation/configuration/plugins.html#styling-properties

You are welcome to change default settings if you want cool stuffs like transparency, gradient
and other. This product use a default configuration that look first of all to high video
accessibility.

Dependencies
============

Dependencies there is a quite long list, but very simple to be satisfied.

Flowplayer Flash plugin needed (provided with the product):

* Flowplayer Captions plugin
* `Flowplayer Contents plugin`__

__ http://flowplayer.org/plugins/flash/content.html

Plone dependencies:

* collective.flowplayer

Plone 3
-------

Plone 3.3 *is supported* with some additional dependencies that are automatically satisfied on
Plone 4:

* `archetypes.schemaextender`__
* `plone.app.blob`__

__ http://pypi.python.org/pypi/archetypes.schemaextender
__ http://pypi.python.org/pypi/plone.app.blob

Quick note on *plone.app.blob*. It works perfectly on Plone 3.3 but maybe that your Plone
configuration is not using it yet.

Without `configuring plone.app.blob`__ you will get an error like this::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 125, in publish
      Module Zope2.App.startup, line 238, in commit
      Module transaction._manager, line 93, in commit
      Module transaction._transaction, line 325, in commit
      Module transaction._transaction, line 424, in _commitResources
      Module ZODB.Connection, line 545, in commit
      Module ZODB.Connection, line 590, in _commit
      Module ZODB.Connection, line 628, in _store_objects
    Unsupported: Storing Blobs in <ZODB.FileStorage.FileStorage.FileStorage object at 0x1025ae090> is not supported.

__ http://pypi.python.org/pypi/plone.app.blob#installation

.. Note::
   You are welcome to help making this product works also on Plone 3 *without* BLOB support.

TODO
====

* A way to display the SubRip source easily (I wrote `collective.subrip2html`__ for this, then I
  saw that it was not really needed for the captioning support...)
* Supporting subtitles also for *Collection* content types (I've problems with the confuse
  Flowplayer APIs)

__ http://plone.org/products/collective.subrip2html/

