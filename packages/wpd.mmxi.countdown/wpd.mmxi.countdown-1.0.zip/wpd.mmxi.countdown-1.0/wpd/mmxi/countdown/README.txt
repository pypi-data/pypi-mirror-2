.. contents:: Table of Contents
   :depth: 2

wpd.mmxi.countdown
****************************************

Overview
--------

A package containing a portlet to display a countdown to the World Plone Day.

Requirements
------------

   * Plone 3.3.x (http://plone.org/products/plone)

   * Plone 4.0.x (http://plone.org/products/plone)
    
Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``wpd.mmxi.countdown``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            wpd.mmxi.countdown

If another package depends on the wpd.mmxi.countdown egg or 
includes its zcml directly you do not need to specify anything in the 
buildout configuration: buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache and save your resource registries
in order to see the effects of the product installation.

Sponsoring
----------

Development of this product was sponsored by `Simples Consultoria 
<http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * André Nogueira (andre at simplesconsultoria.com.br) - Idea, layout

    * Davi Lima (davilima at simplesconsultoria.com.br) - Idea, 
      planning and lines of code
    
    * Érico Andrei (erico at simplesconsultoria.com.br) - Packaging, i18n
    
