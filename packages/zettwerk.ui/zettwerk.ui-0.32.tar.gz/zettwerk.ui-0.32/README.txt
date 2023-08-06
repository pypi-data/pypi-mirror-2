Introduction
============

zettwerk.ui integrates jquery.ui and its themeroller into Plone 4. Themeroller is a tool to dynamically customize the jquery.ui css classes. For details about jquery.ui theming and themeroller see http://jqueryui.com/themeroller/.

See it in action: http://www.youtube.com/watch?v=p4_jU-5HUYA

Use-Cases
=========

With this add-on it is very easy to adapt the look and color scheme of your plone site. Based on the new sunburst Theme, introduced in Plone 4 (it has a nice and clean look). You do not have to create a new skin product, if you just want to change some colors suitable to your CI or for building a quick prototype/mock up.

In addition you will get some of the cool jquery.ui widgets (for example the dialog) integrated in Plone.

Also check out zettwerk.fullcalender for integration of a jquery calender add-on into Plone 4 - which will also use the themeroller customizations.

Feel free to contact us for feedback.

Skins vs Themes
===============

zettwerk.ui is designed to be independet of any particular skin and it is not a skin itself. Once installed, the resources are available for every skin. So it is possible to use zettwerk.ui on top of a custom skin. The only dependencies are the css selectors, which are used to apply the jquery.ui classes. For example: using zettwerk.ui with the classic theme in Plone 4 works, but looks rather bad.

Installation
============

Add zettwerk.ui to your buildout eggs::

  eggs = ..
         zettwerk.ui

After running buildout and starting the instance, you can install Zettwerk UI Themer via portal_quickinstaller to your plone instance. zettwerk.ui requires Plone 4 (tested with 4.0.x and 4.1.x).

Usage
=====

After installation, jquery.ui themes can be applied to some selectable elements of plone. In the plone controlpanel you will find a new extension product listed "Zettwerk UI" which allows you to customize these theme settings. Use the themes tab to create new themes via themeroller or apply one of the example themes from the themeroller galery.

Filesystem dependency
=====================

Created themes are downloaded to the servers filesystem. So a directory is needed, to store these files. At the moment, this is located always relative from your INSTANCE_HOME: ../../zettwerk.ui.downloads. In a common buildout environment, that is directly inside your buildout folder.

Deployment and reuse of themes
==============================

You can easily move the dowloaded themes from the download folder from one buildout instance to another. So to deploy a theme just copy the folder with the name of your theme from your develop server to your live server. It should be immediatelly available (without restart) - but only if the download folder was already created.
