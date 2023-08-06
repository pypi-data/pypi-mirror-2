.. contents:: **Table of contents**

Introduction
============

A Plone utility and view to help you to convert your paths inside site contents.

You can use the new provided utility:

    >>> utility = getUtility(IUIDConverted)
    Do something with the utility methods

Also, a Plone view is provided to automatically fix paths inside documents.

Simply call::

    http://yourplone/folder/subfolder/@@convertUID

Then you can fix all contents in the "*subfolder*" tree.

How is not going well on Kupu feature?
--------------------------------------

The `Kupu`__ project has inside a similar feature for fixing Kupu (and TinyMCE) created
links.

__ http://plone.org/products/kupu

However this not always works, for example, if for some reason you contents have inside absolute
paths like this::

    /plonesite/foo/foo

Also: Kupu is less used in Plone world *and* even if you have it in your Plone environment,
you *must* have it installed and selected as your WYSIWYG editor to use its converting
features.

   .. Warning::
      This product is in early development stage; it will not substitute Kupu migration
      utility and is much less tested.
      
      Use at your own risk... **Data.fs backup** can make difference between life and death 

TODO
====

* Internationalization of the UI
* Plone fixing form needs some love right now
* Much more test
* Beeing a complete alternative to Kupu migration tool
* Also give the "UID to Path" feature
* Relative path conversion is not working for all possibiel path (i.e: '*../foo/a-document*')
* Transformation will not works if linking method/traverse of target object
  (i.e: "foo/image-id/image_thumb")

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

