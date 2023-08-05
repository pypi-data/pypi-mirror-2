Releasing procedure
===================

Prerelease
----------
Go to plone.app.locales directory::

    cd ~/svn/plonenext/4.0.0/src/plone.app.locales

Prepare the release::

    vi CHANGES.txt
    svn ci -m"Prepare release"

or::

    prerelease

Verify there is no error in the po files::

    cd plone/app/locales/locales/
    svn up
    for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done


Release
-------
Do the release (for Plone 3.3.x, use branches/3.x instead of trunk)::

    svn cp https://svn.plone.org/svn/plone/plone.app.locales/trunk \
    https://svn.plone.org/svn/plone/plone.app.locales/tags/4.0.0 -m"Tagged, I'll tag externals on next commit"
    cd /tmp
    svn co https://svn.plone.org/svn/plone/plone.app.locales/tags/4.0.0

You now have to pin PloneTranslations.

First get the revision::

    cd 4.0.0/plone/app/locales/locales
    svn info

You get "Revision: 88537".

Modify the externals accordingly::

    cd ..
    vi EXTERNALS.txt

and remove locales-future.

You should have something like this::
    
    i18n -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/i18n
    locales -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/locales
    locales-addons -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/locales-addons
    utils -r88537 https://svn.plone.org/svn/collective/PloneTranslations/trunk/utils

Set the svn:externals and remove locales-future::

    svn propset svn:externals -F EXTERNALS.txt .
    svn up
    rm -rf locales-future

remove locales-future translations registration in configure.zcml and commit::

    svn ci -m"Pinned revision of PloneTranslations"

    cd /tmp/4.0.0

For Plone 4::

    rm -rf plone/app/locales/i18n

For Plone 3::

    rm -rf plone/app/locales/i18n/kupu

Then::

    cd plone/app/locales/locales/
    for po in `find . -name "*.po"` ; do msgfmt -o `dirname $po`/`basename $po .po`.mo $po; done

    cd -
    python setup.py mregister --strict sdist --formats=zip mupload

Update plone.app.locales version in versions.cfg and etc/versions in
plonenext/3.3.
For Plone 4, update versions.cfg in plone-coredev/branches/4.0 and remove
plone.app.locales from sources.cfg.

Postrelease
-----------

Go back to trunk
Edit setup.py and CHANGES.txt ad commit::

    svn ci -m"Update version after release"

or::

    postrelease
