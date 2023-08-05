beyondskins.ploneday.site2010
=============================

Overview
--------

This product is a installable Plone 3.x, 4.x Theme developed by `Simples
Consultoria <http://www.simplesconsultoria.com.br/>`_.
 
Requirements
------------

    - Plone 4.0 (http://plone.org/products/plone)

    - Plone 3.2.x (http://plone.org/products/plone)
    
    - Plone 3.1.x (http://plone.org/products/plone)

Installation
------------
    
To use this theme, on a buildout based installation:

    1. Unpack beyondskins.ploneday.site2010 package to src/ folder of your 
    buildout
    2. Edit your buildout.cfg and add the following information::

        [buildout]
        ...
        eggs = 
            beyondskins.ploneday.site2010

        [instance]
        zcml = 
            ...
            beyondskins.ploneday.site2010
    
    The last line tells buildout to generate a zcml snippet that tells
    Zope to configure beyondskins.ploneday.site2010.

    If another package depends on the beyondskins.ploneday.site2010 egg or 
    includes its zcml directly you do not need to specify anything in the 
    buildout configuration: buildout will detect this automatically.

    After updating the configuration you need to run the ''bin/buildout'',
    which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache to see the effects of the
product installation.

Browsers and OS's
-----------------
    
    * Internet Explorer 8.0 (WinXP/Vista)
    
    * Internet Explorer 7.0 (WinXP/Vista)
    
    * Firefox 3 (WinXP/Vista/MacOSX)
    
    * Safari 4 (WinXP/Vista/MacOSX)
    
    * Safari 3 (WinXP/Vista/MacOSX)

Credits
-------

* Simples Consultoria (products at simplesconsultoria dot com dot br) - Design / 
  Packaging

