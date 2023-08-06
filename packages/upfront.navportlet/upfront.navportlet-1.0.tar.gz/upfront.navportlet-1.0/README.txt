Introduction
============

upfront.navportlet provides a navigation portlet that uses a dedicated
navigation catalog for it's queries. It is otherwise identical to the
standard Plone navigation portlet.

This portlet uses a dedicated catalog for navigation to ensure that
navigation can work indepentant of the portal_catalog. By using a
separate catalog the indexes and metadata required for navigation is
made explicit.

The development of this portlet was inspired by upfront.diet:
http://www.upfrontsystems.co.za/Members/roche/where-im-calling-from/upfront-diet

Compatibility
=============

Works with Plone 3 and 4.

Installation
============

Please note that this package overrides the standard Plone navigation
portlet.

1. Simply include it as an egg in your buildout and run buildout again:

    [buildout]
    ...
    eggs = upfront.navportlet

There is no need to include it in the zcml section of your buildout
configuration since it uses z3c.autoinclude to install itself.

2. Start your Zope instance and install it using the
portal_quickinstaller.

3. If you install upfront.navportlet into an existing site, you can
reindex all content in your site in the nav_catalog using the Navigation
Portlet configlet in Site Setup.

Custom Content Types
====================

If you have custom content types that need to be displayed in the
Navigation Catalog you need to create a generic setup profile and list
your content types in archetype_tool.xml, eg.:

    <?xml version="1.0"?>
    <archetypetool>
        <catalogmap>
            <type portal_type="MyType">
                <catalog value="portal_catalog"/>
                <catalog value="nav_catalog"/>
            </type>
        </catalogmap>
    </archetypetool>
