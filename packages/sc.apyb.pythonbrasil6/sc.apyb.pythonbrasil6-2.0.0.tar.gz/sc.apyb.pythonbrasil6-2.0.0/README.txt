sc.apyb.pythonbrasil6
=====================

Overview
--------

    Site policy for the upcoming Brazilian Python Convention: PythonBrasil[7].

Requirements
------------

    - Plone 3.3.5 (http://plone.org/products/plone)
    
Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.apyb.pythonbrasil6``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.apyb.pythonbrasil6


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

Development of this product was sponsored by `APyB  
<http://associao.python.org.br/>`_.


Credits
-------

    * Simples Consultoria (products at simplesconsultoria dot com dot br) - 
      Implementation
    
