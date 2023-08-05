====================
stxnext.varnishpurger
====================

Overview
========

Viewlet with action to purge actual url from varnish cache.


Installation
============

If you are using zc.buildout to manage your project, you can do this:

* Add ``stxnext.varnishpurger`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        stxnext.varnishpurger
        
* If you're using plone.recipe.zope2instance recipe to manage your 
  instance add this lines to install a ZCML slug:

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        ...
        stxnext.varnishpurger
           
      
* Re-run buildout, e.g. with::

    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.

Finally go to portal_setup and import steps for stxnext.varnishpurger profile.

Usage
=====

After installation one new viewlet above object's content will be displayed.
The viewlet contains a link to purge content of actual url from varnish cache.
In site properties there is additional configuration for varnish url and
domains to be purged.

The varnish configuration file should contain customized vcl_recv subroutine
to purge given object by it's UID.
 
sub vcl_recv {

	...

   if (req.request == "PURGE") {
        if (!client.ip ~ purge) {
             error 405 "Not allowed.";
	    }
        purge("obj.http.X-Context-Uid ~ " req.url);
   	    error 200 "Purged";
        return(lookup);
   }
    
    ...

}

References
==========

.. varnish: http://varnish.projects.linpro.no/
.. Plone: http://plone.org



Author & Contact
================

:Author:
 * Radosław Jankiewicz <``radoslaw.jankiewicz@stxnext.pl``>
 * Wojciech Lichota <``wojciech.lichota@stxnext.pl``>
 * Marcin Ossowski <``marcin.ossowski@stxnext.pl``>

.. image:: http://stxnext.pl/open-source/files/stx-next-logo

**STX Next** Sp. z o.o.

http://stxnext.pl

info@stxnext.pl