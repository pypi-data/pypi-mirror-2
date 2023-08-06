.. -*-doctest-*-

===================
collective.redirect
===================

Administer redirects to internal or external URLs using Link like
content.  Where Products.redirectiontool or plone.app.redirector only
deal with redirecting to internal URLs internal to the portal,
collective.redirect allows for redirecting to external URLs.  The
paths to redirect are administered using instances of the Redirect
content type.  The paths that are redirected are independent of the
path of the Redirect instance for a couple of reasons.

Firstly, since the portal object is not a BTree based folder it will
begin to behave poorly if too many objects are added to it.  Allowing
the redirected paths independent from the location of the Redirect
instances allows for many redirects without putting too many objects
in the portal root.

Secondly, having the paths independent of the Redirect instance
locations allows users to create redirect for paths that they can't
add content too.  Keep in mind that this might be a bad thing for your
site and can certainly be abused as a DOS attack of sorts.

If multiple redirects exist for the same path, the one with the more
recent publication date will be preferred.  Finally a redirect will
never override an otherwise traversable URL.  IOW, a redirect cannot
override an actual content object, skin object, view, or anything else
traversal.  The redirect only occurs when a NotFound error would
otherwise be raised.

Use a browser.

    >>> from Products.Five import testbrowser
    >>> browser = testbrowser.Browser()
    >>> portal.error_log._ignored_exceptions = ()
    >>> portal_url = portal.absolute_url()

Before a redirect is added, going to a non-existent URL will return
the 404 page.

    >>> browser.open(portal_url+'/foo')
    Traceback (most recent call last):
    HTTPError: HTTP Error 404: Not Found
    
    >>> browser.open(portal_url+'/bar')
    Traceback (most recent call last):
    HTTPError: HTTP Error 404: Not Found
    
Open another browser and login as a user who can add Redirects.

    >>> from Products.PloneTestCase import ptc
    >>> member_browser = testbrowser.Browser()
    >>> member_browser.handleErrors = False
    >>> member_browser.open(portal.absolute_url())
    >>> member_browser.getLink('Log in').click()
    >>> member_browser.getControl(
    ...     'Login Name').value = ptc.default_user
    >>> member_browser.getControl(
    ...     'Password').value = ptc.default_password
    >>> member_browser.getControl('Log in').click()
    >>> member_browser.open(portal_url+'/Members/test_user_1_')

Add a redirect.  Set the "Local Path" field to the path that should be
redirected from.  The local path is always rooted at the portal.  Set
the "URL" field to the URL that should be redirected to.

    >>> member_browser.getLink(url='createObject?type_name=Redirect').click()
    >>> member_browser.getControl('Title').value = 'Foo Redirect Title'
    >>> member_browser.getControl('Local Path').value = '/foo'
    >>> member_browser.getControl('URL').value = '/plone/events'
    >>> member_browser.getControl('Save').click()
    >>> print member_browser.contents
    <...
    ...Changes saved...
    ...Foo Redirect Title...
    ...Local Path...
    .../foo...
    ...URL...
    .../events...

When the redirect is not accessible to the user visiting the local
path, such as when the workflow of the redirect forbids it, the
redirect will not occur.

    >>> foo_redirect = portal.Members.test_user_1_['foo-redirect-title']
    >>> portal.portal_workflow.getInfoFor(
    ...     foo_redirect, 'review_state')
    'private'
    >>> browser.open(portal_url+'/foo')
    Traceback (most recent call last):
    HTTPError: HTTP Error 404: Not Found
    
Once the redirect is accessible, the user visiting the local path is
redirected to the remote URL.

    >>> self.loginAsPortalOwner()
    >>> portal.portal_workflow.doActionFor(foo_redirect, 'publish')
    >>> self.logout()

Use a VHM style URL to simulate a virtual hosting environment.

    >>> browser.open('http://nohost/VirtualHostBase/http/nohost'
    ...              '/VirtualHostRoot/plone/foo/')
    >>> browser.url
    'http://nohost/plone/events'

A local path that has no redirect still returns the 404 page.

    >>> browser.open(portal_url+'/bar')
    Traceback (most recent call last):
    HTTPError: HTTP Error 404: Not Found

Now, let's make sure that a redirect with two or more levels of non-existent
path segments still works as expected.

    >>> member_browser.open(portal_url+'/Members/test_user_1_')
    >>> member_browser.getLink(url='createObject?type_name=Redirect').click()
    >>> member_browser.getControl('Title').value = 'Foo Redirect Two Segments'
    >>> member_browser.getControl('Local Path').value = '/foo/some/path'
    >>> member_browser.getControl('URL').value = '/plone/news'
    >>> member_browser.getControl('Save').click()
    >>> self.loginAsPortalOwner()
    >>> foo_redirect_two_segments = portal.Members.test_user_1_['foo-redirect-two-segments']
    >>> portal.portal_workflow.doActionFor(foo_redirect_two_segments, 'publish')
    >>> self.logout()
    >>> browser.open('http://nohost/VirtualHostBase/http/nohost'
    ...              '/VirtualHostRoot/plone/foo/some/path')
    >>> browser.url
    'http://nohost/plone/news'

