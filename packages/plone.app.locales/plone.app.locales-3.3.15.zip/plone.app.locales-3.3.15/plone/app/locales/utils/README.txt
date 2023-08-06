Preparing Plone 3.3 buildout
============================
mkdir ~/svn
cd ~/svn
svn co https://svn.plone.org/svn/plone/plone-coredev/branches/3.3/ plone3
cd plone3
bin/sync-with-plonenext
python bootstrap.py
bin/buildout -c i18n.cfg
mkdir Products
cd src
ln -s Plone Products.CMFPlone
cd plone.app.locales/plone/app/locales/utils
export INSTANCE_HOME=~/svn/plone3


Updating translations
=====================
plone
-----
::

    python rebuild-pot.py plone
    python sync.py plone

atcontenttypes
--------------
::

    python rebuild-pot.py atct
    python sync.py atcontenttypes


atreferencebrowserwidget
------------------------
::
    python rebuild-pot.py atrbw
    python sync.py atreferencebrowserwidget

passwordresettool
-----------------
::

    python rebuild-pot.py prt
    python sync.py passwordresettool

cmfplacefulworkflow
-------------------
::

    python rebuild-pot.py cmfpw
    python sync.py cmfplacefulworkflow

cmfeditions
-----------
::

    python rebuild-pot.py cmfe
    python sync.py cmfeditions

kupu
----
::

    python rebuild-pot.py kupu
    python sync.py kupu

    python rebuild-pot.py kupuconfig
    python sync.py kupuconfig

    python rebuild-pot.py kupupox
    python sync.py kupupox

linguaplone
-----------
::

    python rebuild-pot.py lp
    python sync.py linguaplone

plonefrontpage
--------------
::

    cd locales
    i18ndude sync --pot plonefrontpage.pot */*/plonefrontpage.po


SVN externals
=============
::

    plone.app.locales/trunk -> PloneTranslations/trunk
    plone.app.locales/branches/3.x -> PloneTranslations/branches/3.x
    plone.app.locales/branches/3.x/i18n/kupu -> PloneTranslations/trunk/i18n/kupu
    Product.kupu/trunk/i18n -> PloneTranslations/trunk/i18n/kupu
