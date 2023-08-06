.. contents:: Table of Contents
   :depth: 2

Products.CMFPublicator
**************************

Overview
--------

This product was born at 2004/01/15 and provide a tool used to do static
content publication in CMF and Plone sites. It broke with CMF's idea of free
showing published content according to pre-defined rules, giving to the
reviewer power to choose just the objects he wants to show in the portlets.


Requirements
------------

    - Plone >= 3.2.x (http://plone.org/products/plone)

Installation
------------

To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``Products.CMFPublicator``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs =
            Products.CMFPublicator

    2. Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

        [instance]
        ...
        zcml =
            ...
            Products.CMFPublicator

If another package depends on the Products.CMFPublicator egg or
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


Usage
-----

When you have followed the doc/INSTALL.txt file and installed CMFPublicator
succesfully, you must setup which publication boxes the portal will have:

  1. Go to ZMI of your portal root

  2. Go to the 'portal_publicator' tool

  3. There are a tab containing the settings for configuration:

     The 'Configuration' tab contains the fields to insert new publication
     boxes.

     Make one publication box to each portlet box that you want to have.

  4. Each publication box created needs an integrated portlet_interface
     to interact with us. This interface can be customized in default
     portal_skins folder.

     Follows the idea of this portlet to make and customize others, and
     have fun! ;-)

Having problems to setup CMFPublicator?
You can ask questions at jeanrodrigoferri@yahoo.com.br

Having general Zope problems?
Visit http://www.zope.org/Resources


Sponsoring
----------

Eggfication of this product was sponsored by `Simples Consultoria
<http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Jean Rodrigo Ferri - jeanrodrigoferri@yahoo.com.br (main developer)
    
    * Gustavo Lepri - gustavolepri@gmail.com

    * Clayton Caetano de Sousa - claytonc.sousa@gmail.com

    * Davi Lima de Medeiros - davilima6@gmail.com

    * Luís Flávio Loreto da Rocha - lflrocha@gmail.com

    * Paulo Henrique Balzi - paulohbg@yahoo.com.br

    * Paulo Henrique Vieira - phgvieira@uol.com.br

    * Rafahela Garcia Bazzanella - rafabazzanella@yahoo.com.br

    * Rodrigo Dias Arruda Senra - rodsenra@gpr.com.br

    * Wilton Souza Alencar - wiltonsa@yahoo.com.br

