Introduction
============

This package add a new view to Plone's Link content type. If the remote url of
the link is video supported by p4a.videoembed it will display the embed video.

.. contents::


Credits
======================================
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com


Dependencies
============

* Plone
* p4a.videoembed

Why this package ?
==================

p4a.plonevideoembed depends on p4a.video that has too much dependecies and too
much features (subtype, metadata, ...).

TODO
====

* Make configuration for the default fall back view (at the moment 'link_redirect_view' is hard coded)
