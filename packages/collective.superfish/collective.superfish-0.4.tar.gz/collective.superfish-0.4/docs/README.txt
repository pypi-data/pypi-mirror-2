====================
collective.superfish
====================

.. contents::

What is it?
===========

collective.superfish is an suckerfish integration into Plone. Suckerfish is a
really nice solution for dropdown menus using css, valid xhtml and javascript.
http://www.alistapart.com/articles/dropdowns/


How do i use it?
================

Hide `plone.global_sections` and replace it with `collective.superfish`
in viewlets.xml somehow like this::

    <!-- superfish: use superfish instead of global_sections -->
    <hidden manager="plone.portalheader" skinname="MySkin">
        <viewlet name="plone.global_sections" />
    </hidden>

    <order manager="plone.portalheader" skinname="MySkin">
        <viewlet name="collective.superfish" insert-after="plone.global_sections" />
    </order>


By default, `collecive.superfish` does not include portal_actions in the menu.
To activate them, subclass the viewlet::

    from collective.superfish.browser.sections import SuperFishViewlet as SuperFishBase

    class SuperFishViewlet(SuperFishBase):

        ADD_PORTAL_TABS = True

and register it for your skin::

    <browser:viewlet
        name="collective.superfish"
        manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
        class=".viewlets.SuperFishViewlet"
        permission="zope2.View"
        layer=".interfaces.IThemeSpecific"/>


