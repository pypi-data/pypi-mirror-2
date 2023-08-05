Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url + '/login_form')

Here, we set the value of the fields on the login form and then simulate a
submit click.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()


And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, we go to the home page
    >>> browser.open(portal_url)


-*- extra stuff goes here -*-
The Image content type
===============================

Adding a new Image content item
--------------------------------


We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Image' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Image').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Image' in browser.contents
    True

Now we fill the form with a png file and submit it.

    >>> import os
    >>> from App import Common
    >>> pkg_home = Common.package_home({'__name__': 'collective.atimage.transformmenu'})
    >>> samplesdir = os.path.join(pkg_home, 'tests', 'samples')
    >>> browser.getControl(name='image_file').add_file( \
    ... file(os.path.join(samplesdir, 'test_image.png')).read(), \
    ... 'image/png', 'test_image.png')
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Now we test the Transform new menu::

Given that this product hides the "Transform" content-view tab, we should get an error when getting the "Transform" tab link
    >>> browser.getLink('Transform')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

In spite, there should be a Transform label present in page

    >>> '<span class="label">Transform</span>' in browser.contents
    True

Now we make sure we are in the 'View' tab of the Image before transforming the image in any possible way, to end up in the same View page
    >>> browser.getLink('View').click()
    >>> view_url = browser.url
    >>> browser.getLink(url='/@@transform?method:int=0').click()
    >>> browser.getLink(url='/@@transform?method:int=1').click()
    >>> browser.getLink(url='/@@transform?method:int=2').click()
    >>> browser.getLink(url='/@@transform?method:int=3').click()
    >>> browser.getLink(url='/@@transform?method:int=4').click()
    >>> browser.url == view_url
    True
