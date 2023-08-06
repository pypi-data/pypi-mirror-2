Introduction
============

Creating a photo album or gallery in Plone is easy, just see `Create a photo
album`__.

This products makes it possible to include a gallery in a regular page. 
It does this through javascript.

Usage
=====

When editing your page's text in the text editor, add an internal link to the
folder that contains your photos (your gallery).

Go into the HTML editor by clicking the editor's HTML button, and add a class
`InlinePhotoAlbum` to the link.

The link will be replaced by a rendering of the gallery. This is done by
javascript, so if javascript is disabled, it will just display the link.

When clicked, the photos will be displayed in an overlay.

Features
========

- Open photos in overlay
- Batching

Install
=======

Add `Products.InlinePhotoAlbum` to your buildout.

Compatibility
=============

Tested on Plone 4.

Credits
=======

- Huub Bouma (creator)
- Kees Hink (maintainer)

.. _create-a-photo-album: http://plone.org/documentation/kb/create-a-photo-album
__ create-a-photo-album_
