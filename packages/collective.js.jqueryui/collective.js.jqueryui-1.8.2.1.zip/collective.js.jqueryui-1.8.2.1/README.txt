Introduction
============

Integration of jqueryui in Plone 4.
Use 1.7.2.7 versions if you want to use this package on Plone < 4.

This version includes jqueryui 1.8.2 without the tabs plugin. The Smoothless
theme is used.

It is different from collective.jqueryui in many ways:

* no skin dirs (js and css are in resource dirs)
* no all the bunch of files and documentations from original jqueryui
* this one is minified
* just add all jqueryui to portal_js, and default css to portal_css (if you 
  apply the profile)


Credits
=======

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_
* Contributions by Vincent Fretin (`Ecreall <http://www.ecreall.com>`_)

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com


Notes
=====

The package contains now only one profile. It doesn't replace
the jQuery version like the previous versions did.

Upgrade notes
=============

If you used the ``withjqtools`` or ``withjqtoolsplone3`` profile in older
version, please use now the ``default`` profile.
