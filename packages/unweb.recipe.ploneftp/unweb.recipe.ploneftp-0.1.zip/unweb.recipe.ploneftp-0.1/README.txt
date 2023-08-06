Introduction
============

A zc.buildout recipe for Plone sites that configures an ftp upload proxy with
resume support in front of Zope's Medusa FTP. Plone users can login using their
username and password. When a file is succefully uploaded it is moved to the 
user's home folder in Plone.

- Code repository: http://svn.plone.org/svn/collective/unweb.recipe.ploneftp/
- Questions and comments to https://unweb.me/contact
- Report bugs at http://plone.org/products/unweb.recipe.ploneftp/issues


Supported options
-----------------

The recipe supports the following options:
::

    address
        host and port to listen on. Defaults to port 21

    zope_ftp_address
        host and port of the zope ftp. Defaults to 127.0.0.1:8021

    path
        path of the target folder in Zope. Defaults to /Plone/Members/%s where %s is the username

    tmp_dir
        temporary directory where files will be uploaded. Defaults to /tmp/PloneFTP

    login_message
        custom login message. Defaults to "Welcome to Plone FTP. Your uploaded file may not be visible in FTP when the upload has finished. Go to your Plone site member folder to see your file."

    logout_message
        custom logout message. Defaults to "Thanks for using Plone FTP!"


Credits
-------

Created by `unweb.me`_

.. _unweb.me: https://unweb.me

Based on `plumiftp`_ by Andy Nicholson and Victor Rajewski.

.. _plumiftp: http://pypi.python.org/pypi/plumiftp

Development sponsored by `engagemedia.org`_

.. _engagemedia.org: http://engagemedia.org

