inqbus.zopeftp
==============

Overview
--------

inqbus.zopeftp add a config parameter which can be used in zope.conf (Zope 2), that allow one to configure a start path for ftp users, like the path to a plone site. Then if you use a ftp-client to connect to your zope, first the directory is change to the configured path and then the user is authentificated there. So it's enough that the user exist in this place (in a plone site for example), there is no need anymore to add this member in the zope root acl_users. 


Install inqbus.zopeftp
----------------------

Add inqbus.zopeftp to you eggs and zcml lists in you buildout.cfg::
eggs = 
    inqbus.zopeftp

zcml =
    inqbus.zopeftp


Set the FTP start path
----------------------

You can add the folowing config entry in your buildout.cfg::

    zope-conf-additional =
        <product-config inqbus.zopeftp>
            ftppath site/ftp-docs
        </product-config>

or just add these lines to your zope.conf::

    <product-config inqbus.zopeftp>
        ftppath site/ftp-docs
    </product-config>
