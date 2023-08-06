Introduction
============

You are a site administrator? Maybe you already saw use cases below.

Use case one

    "Hi, I deleted an importan content created yesterday. I created it back
    but for $INTERNAL reason I need that this content seems created yesterday,
    before 02:00 P.M."
    
    -- a user

Use case two

    "Hi, I accidentally modified an old document... or better: the change was
    needed but for $INTERNAL reason I need it seems again 'old' ad before.
    Can you restore the last modification date to January 2008?"
    
    -- another user

Epilogue
--------

The collective.datehacker product add to Plone a simple new view that you (the site admin? a smart
user? every users in the portal) can use to change two of the most untouchable date inside Plone
contents: the **modification date** and the **creation date**.

If you are trained enough, you can change those dates in few lines of code, but maybe:

* you don't know how to write code
* you are lazy
* you don't have an account with *Manager* permissions
* none of above, but you are sure that, sooner or later, someone will ask again for the same
  change.

Also this product can be useful after some big-migration activiti to Plone. May be that you or
your users need to be able to restore some creation/modification date after the process.

Instructions
============

No much to say, just call an URL like http://myplonesitehost/mycontenttype/hackdates then
you can use the user friendly form

.. image:: http://keul.it/images/plone/collective.datehacker-0.1.0a.png
   :alt: The Plone form for changing dates

The form can only be called from users that behave the "*Hack content's dates*" permission.

You can call the **hackdates** views where you want.

TODO
====

* Register someway, somewhere, the hacking operation
* Test on Plone 4 (it must work, but is untested)

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

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
