Introduction
============
The solely intention of this product is to replace the default "Transform" tab in Image and News Item content types with an icon-toolbar viewlet in the plone.abovecontentbody viewlet manager.

By keeping the user in the same page and requiring less clicks and page loads we intend to ease applying transformations in the images.

Features
========

- Toolbar is in plone.abovecontentbody viewlet manager for Image and News Item
- Performs image transformations with AJAX to prevent reloading the page
- Degrades gracefully in non-JavaScript browsers
- i18n support by using atcontentypes and plone i18n domains.
- Tested in Plone 3.3.5 and Plone 4.0b5

TODO
====

- Extend test with new case for News Items
