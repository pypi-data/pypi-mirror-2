Plone Hotfix package, 2011-05-31
********************************

This hotfix fixes the following four vulnerabilities:

1. Reflected XSS attack: A crafted URL can display arbitrary HTML output.
   This is a vulnerability in CMFPlone affecting all versions of Plone.
   Thanks to **S. Streichsbier** of *SEC Consult* for the responsible
   disclosure.
   See `CVE-2011-1948`_ for details.

2. Persistent XSS attack: Certain valid HTML will allow Javascript filtering to
   be bypassed.  This is a vulnerability in Products.PortalTransforms affecting
   all versions of Plone using it, including 2.1 through 4.1.  Thanks to 
   **Daniel Berlin** and **Dan Bentley** both of *Google* and  **Brian Peters** 
   an independent researcher, for responsibly disclosing this independently of 
   each other.
   See `CVE-2011-1949`_ for details.

3. Unauthorized data changes: One form allows users to edit the properties of
   other users. This is a vulnerability in plone.app.users affecting Plone 4.0
   and 4.1. 
   This vulnerability was not disclosed responsibly to the security team.
   See `CVE-2011-1950`_ for details.

4. Denial of service: A user can prevent other users from logging in. This is
   a vulnerability in Products.PluggableAuthService affecting all versions of
   Plone using it, including 2.5 through 4.1. Thanks to **Alan Hoey** of
   *Team Rubber* for the responsible disclosure.
   See `PAS ticket #789858`_ for details.

.. _`CVE-2011-1948`: http://plone.org/products/plone/security/advisories/CVE-2011-1948
.. _`CVE-2011-1949`: http://plone.org/products/plone/security/advisories/CVE-2011-1949
.. _`CVE-2011-1950`: http://plone.org/products/plone/security/advisories/CVE-2011-1950
.. _`PAS ticket #789858`: https://bugs.launchpad.net/zope-pas/+bug/789858

This hotfix is supported on Plone 3 and 4.  It is also known to work on Plone
2.5, and may work on older versions of Plone.

The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.0.7, 4.1rc3, and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
http://plone.org/products/plone-hotfix/releases/20110531

Changelog
=========

1.0 (2011-06-01)
----------------

- Initial release
  [Plone security team]
