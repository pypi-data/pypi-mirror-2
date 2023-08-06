Tests
=========
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

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

The Map Content content type
------------------------------------
In this section we are tesing the Map Content content type by performing
basic operations like adding, updadating and deleting Map Content content
items.

Adding a new Map Content content item
++++++++++++++++++++++++++++++++++++++++
We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Map Content').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'Map Content Sample'
    >>> js = """
    ... jq('#mapcontent').css('height', '1024px');
    ... jq('#mapcontent').css('width', '1024px');
    ... var coords = {lon: 0.000000, lat: 0.000000, zoom: 10};
    ... cgmap.state = {'default': coords, 'mapcontent': coords};
    ... cgmap.extendconfig(
    ...   {layers: [function() {
    ...                  return new OpenLayers.Layer.WMS("OpenLayers WMS", "http://vmap0.tiles.osgeo.org/wms/vmap0", {layers: 'basic'});}
    ...            ]
    ...   },
    ...   'mapcontent');
    ... """
    >>> browser.getControl(name='_js').value = js
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Rendering
+++++++++++++
And we are done! We added a new 'Map Content' content item to the portal and in view mode, it will render using the mapwidget macros

    >>> '<script type="text/javascript">'+js in browser.contents
    True

.. vim:set ft=rest:
