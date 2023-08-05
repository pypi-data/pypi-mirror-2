==============================================================================
Test Deliverance Theme Selector Use
==============================================================================

Create the browser object we'll be using.

    >>> from Products.Five.testbrowser import Browser
    >>> from DateTime.DateTime import DateTime
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()

Log in into the site as manager.

    >>> from Products.PloneTestCase.setup import portal_owner, default_user, default_password
    >>> login_url = portal_url + '/login_form'
    >>> logout_url = portal_url + '/logout'
    >>> browser.open(login_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

We will go into the product configuration

    >>> sitesetup_url = portal_url + '/plone_control_panel'
    >>> browser.open(sitesetup_url)
    >>> browser.getLink('Deliverance Theme Selector').click()
    >>> "List of available themes to use with deliverance" in browser.contents
    True

Add a few themes and css class in the product's registry

    >>> browser.getControl('Add').click()
    >>> browser.getControl(name='form.widgets.availableThemes.0').value = 'ThemeA:ClassA'
    >>> browser.getControl('Add').click()
    >>> browser.getControl(name='form.widgets.availableThemes.1').value = 'ThemeB:ClassB'
    >>> browser.getControl('Add').click()
    >>> browser.getControl(name='form.widgets.availableThemes.2').value = 'ThemeC:ClassC'
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

Create a container object named 'folder0' in the portal root

    >>> browser.open(portal_url)
    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Folder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'folder0'
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

    >>> folder0_url = browser.url

Enable Deliverance Theme Selector in the new object 'folder0'

    >>> # browser.getLink('Actions')
    >>> browser.getLink('Enable DTS').click()
    >>> "Enable Deliverance Theme Selector for this section" in browser.contents
    True

Now Confirm the action

    >>> browser.getControl('Save').click()
    >>> "Deliverance theme selector enable" in browser.contents
    True

Select the Class for this Section

    >>> ctrl = browser.getControl(name='form.widgets.theme:list')

The first option is selected by default

    >>> ctrl.getControl('ClassA').selected
    True

So we are going to use that option, and save the form

    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

Open the 'folder0' object and see if the 'X-Deliverance-Page-Class' header is there

    >>> browser.open(folder0_url)
    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeA'

Now we are going to create second level object inside the object'folder0'

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Folder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'folder1'
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

    >>> folder1_url = browser.url

We can see that the 'X-Deliverance-Page-Class' is inherited from the parent object

    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeA'

Change the css class in the 'DTS Settings' for the 'folder0' object

    >>> browser.open(folder0_url)
    >>> browser.getLink('DTS Settings').click()
    >>> browser.url
    'http://nohost/plone/folder0/@@dts-settings'

    >>> ctrl = browser.getControl(name='form.widgets.theme:list')
    >>> ctrl.getControl('ClassB').click()
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

And now we can see the new 'X-Deliverance-Page-Class' header

    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeB'

Open the 'folder1' object and see if the 'X-Deliverance-Page-Class' header change too

    >>> browser.open(folder1_url)
    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeB'

Enable Deliverance Theme Selector in the object 'folder1'

    >>> # browser.getLink('Actions')
    >>> browser.getLink('Enable DTS').click()
    >>> "Enable Deliverance Theme Selector for this section" in browser.contents
    True

Confirm the action

    >>> browser.getControl('Save').click()
    >>> "Deliverance theme selector enable" in browser.contents
    True

And select the Class for this Section

    >>> ctrl = browser.getControl(name='form.widgets.theme:list')
    >>> ctrl.getControl('ClassC').click()
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

And now we can see the 'X-Deliverance-Page-Class' header that we set in last step for this object

    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeC'


Now we are going to create third level object inside of 'folder1'

    >>> browser.getLink('Add new').click()
    >>> browser.getControl('Folder').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> browser.getControl(name='title').value = 'folder2'
    >>> browser.getControl('Save').click()
    >>> "Changes saved" in browser.contents
    True

    >>> folder2_url = browser.url

We can see that the 'X-Deliverance-Page-Class' is inherited from the parent object

    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeC'

But what happens if we disable the DTS support in the parent object? Let see

    >>> browser.open(folder1_url)
    >>> # browser.getLink('Actions')
    >>> browser.getLink('Disable DTS').click()
    >>> "Disable Deliverance Theme Selector for this section" in browser.contents
    True

Confirm the action

    >>> browser.getControl('Save').click()
    >>> "Deliverance theme selector disable" in browser.contents
    True

And now open the 'folder2' object and look its headers

    >>> browser.open(folder2_url)
    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeB'

The same happens in the object 'folder1', both are taking the header from the object 'folder0'

    >>> browser.open(folder2_url)
    >>> browser.headers['X-Deliverance-Page-Class']
    'ThemeB'
