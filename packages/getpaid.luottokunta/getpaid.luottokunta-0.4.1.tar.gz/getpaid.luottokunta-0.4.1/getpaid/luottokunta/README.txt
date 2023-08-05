    >>> from Products.CMFCore.utils import getToolByName

Setting up and logging in
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> portal_url
    'http://nohost/plone'

For debugging
    >>> browser.handleErrors = True
    >>> self.portal.error_log._ignored_exceptions = ()

Turn off portlets
    >>> from zope.component import getUtility, getMultiAdapter
    >>> from plone.portlets.interfaces import IPortletManager
    >>> from plone.portlets.interfaces import IPortletAssignmentMapping

    >>> left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
    >>> left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
    >>> for name in left_assignable.keys():
    ...     del left_assignable[name]

    >>> right_column = getUtility(IPortletManager, name=u"plone.rightcolumn")
    >>> right_assignable = getMultiAdapter((self.portal, right_column), IPortletAssignmentMapping)
    >>> for name in right_assignable.keys():
    ...     del right_assignable[name]

Log in as the portal owner. We do this from the login page.
    >>> browser.open(portal_url)
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url + '/login_form?came_from=' + portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> try:
    ...     browser.getControl(name='submit').click()
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()

    >>> browser.open(portal_url)

=============================================================================================
First install PloneGetPaid.
    >>> installer = getToolByName(portal, 'portal_quickinstaller')
    >>> installer.isProductAvailable('PloneGetPaid')
    True
    >>> self.portal.portal_quickinstaller.installProduct('PloneGetPaid')
    ''
    >>> len(installer.listInstalledProducts())
    1

    >>> try:
    ...     browser.open(portal_url)
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()


Testing the setup aspects of GetPaid. Setting required settings.
    >>> browser.open(portal_url)
    >>> browser.getLink('Site Setup').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Site Profile').click()
    >>> browser.getControl('Contact Email').value = 'info@plonegetpaid.com'
    >>> browser.getControl( name="form.store_name").value = 'Test this fake company'

Note: setting 'displayValue = ['UNITED STATES']' would give an
AmbiguityError as the browser does not understand that we do not mean
'UNITED STATES MINO' which is also an option.  So we set an
unambiguous value::

    >>> browser.getControl('Apply').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Content Types').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Payment Options').click()

    >>> browser.getControl(name = 'form.payment_processor').displayValue = ['Luottokunta Processor']

    >>> browser.getControl(name = 'form.allow_anonymous_checkout').value = 'on'
    >>> browser.getControl('Apply').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Payment Processor Settings').click()
    >>> fields_name = ['Merchant Number', 'Card Details Transmit', 'Transaction Type', 'Use Authentication MAC', 'Authentication MAC', 'Use Incremenatal Order Number', 'Next Order ID']
    >>> for field in fields_name:
    ...     field in browser.contents 
    True
    True
    True
    True
    True
    True
    True
    >>> browser.getControl(name="form.merchant_number").value = '123456'
    >>> browser.getControl(name="form.card_details_transmit").value = ''
    >>> browser.getControl(name="form.transaction_type").value = ''
    >>> browser.getControl('Apply').click()
    >>> browser.getLink('GetPaid').click()

Here we are setting the donate type for use in the following tests
    >>> from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
    >>> options = IGetPaidManagementOptions(self.portal)
    >>> options.donate_types = ['Document']

Check to make sure the settings we put in Site Profile appear on this page. 
     >>> browser.getLink('Home').click()

Setup Donatable
    >>> browser.getLink('Make this a Donation').click()
    >>> browser.getControl(name='form.donation_text').value = 'Test donation description'
    >>> browser.getControl(name='form.price').value = '11.00'
    >>> browser.getControl('Activate').click()

Test donation checkout, which should go directly to checkout screen from the portlet. 
    >>> browser.getLink('Donate!').click()
    >>> saved_url = browser.url

Continue where we left of after clicking Donate.
    >>> browser.open(saved_url)
    >>> browser.getControl('Your Name').value = 'Test'
    >>> browser.getControl('Phone Number').value = '1234567'
    >>> browser.getControl('Phone Number').value = '12345678'
    >>> browser.getControl(name='form.email').value = 'test@test.com'
    >>> browser.getControl(name='form.bill_name').value = 'Test'
    >>> browser.getControl(name='form.bill_first_line').value = 'Test'
    >>> browser.getControl(name='form.bill_city').value = 'Test'
    >>> browser.getControl(name='form.bill_state').value = ('US-HI',)
    >>> browser.getControl(name='form.bill_postal_code').value = '12345'
    >>> browser.getControl(name='form.ship_first_line').value = 'Test'
    >>> browser.getControl(name='form.ship_city').value = 'Test'
    >>> browser.getControl(name='form.ship_state').value = ('US-HI',)
    >>> browser.getControl(name='form.ship_postal_code').value = '12345'

Now go to the next form.
    >>> try:
    ...     browser.getControl('Continue').click()
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()


    >>> "id=\"Merchant_Number\" value=\"123456\"" in browser.contents
    True
    >>> "id=\"Card_Details_Transmit\" value=\"0\"" in browser.contents
    True
    >>> "id=\"Language\"" in browser.contents
    True
    >>> "value=\"EN\"" in browser.contents
    True
    >>> "id=\"Transaction_Type\" value=\"0\"" in browser.contents
    True
    >>> order_id = browser.getControl(name="Order_ID").value
    >>> thanks_url = "http://nohost/plone/@@luottokunta-thank-you?getpaid_order_id=%s" %(order_id)
    >>> thanks_url in browser.contents
    True
    >>> "http://nohost/plone/@@luottokunta-cancelled" in browser.contents
    True
    >>> "http://nohost/plone/@@luottokunta-declined" in browser.contents
    True
    >>> "id=\"Authentication_Mac\"" in browser.contents
    False
    >>> ("value=\"%s\"" %(order_id)) in browser.contents
    True
    >>> "value=\"1100\"" in browser.contents
    True


    >>> browser.open(portal_url)
    >>> browser.getLink('Site Setup').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Payment Processor Settings').click()

    >>> browser.getControl('Card Details Transmit').selected = True
    >>> browser.getControl('Transaction Type').selected = True
    >>> browser.getControl('Use Authentication MAC').selected = True
    >>> browser.getControl('Use Incremenatal Order').selected = True
    >>> browser.getControl('Apply').click()
     >>> browser.getLink('Home').click()
    >>> browser.getLink('Donate!').click()
    >>> saved_url = browser.url

Continue where we left of after clicking Donate.
    >>> browser.open(saved_url)
    >>> browser.getControl('Your Name').value = 'Test'
    >>> browser.getControl('Phone Number').value = '1234567'
    >>> browser.getControl('Phone Number').value = '12345678'
    >>> browser.getControl(name='form.email').value = 'test@test.com'
    >>> browser.getControl(name='form.bill_name').value = 'Test'
    >>> browser.getControl(name='form.bill_first_line').value = 'Test'
    >>> browser.getControl(name='form.bill_city').value = 'Test'
    >>> browser.getControl(name='form.bill_state').value = ('US-HI',)
    >>> browser.getControl(name='form.bill_postal_code').value = '12345'
    >>> browser.getControl(name='form.ship_first_line').value = 'Test'
    >>> browser.getControl(name='form.ship_city').value = 'Test'
    >>> browser.getControl(name='form.ship_state').value = ('US-HI',)
    >>> browser.getControl(name='form.ship_postal_code').value = '12345'

Now go to the next form.
    >>> try:
    ...     browser.getControl('Continue').click()
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()

    >>> "id=\"Card_Details_Transmit\" value=\"1\"" in browser.contents
    True
    >>> "id=\"Language\"" in browser.contents
    False
    >>> "id=\"Transaction_Type\" value=\"1\"" in browser.contents
    True
    >>> order_id = browser.getControl(name="Order_ID").value
    >>> order_id == '1'
    True
    >>> state = "REVIEWING"
    >>> thanks_url = "http://nohost/plone/@@luottokunta-thank-you?order_id=%s&amp;finance_state=%s" %(order_id, state)
    >>> ("value=\"%s\"" %(thanks_url)) in browser.contents
    False
    >>> "id=\"Authentication_Mac\"" in browser.contents
    False
    >>> ("value=\"%s\"" %(order_id)) in browser.contents
    True
    >>> "value=\"2200\"" in browser.contents
    True

Now input authentication mac and next order id.

#    >>> browser.open("http://nohost/plone/@@luottokunta_payment_settings_page")

    >>> browser.open(portal_url)
    >>> browser.getLink('Site Setup').click()
    >>> browser.getLink('GetPaid').click()
    >>> browser.getLink('Payment Processor Settings').click()


    >>> browser.getControl(name="form.authentication_mac").value = 'abcdef'
    >>> browser.getControl('Next Order ID').value = '10'
    >>> browser.getControl('Apply').click()
     >>> browser.getLink('Home').click()
    >>> browser.getLink('Donate!').click()
    >>> saved_url = browser.url

Continue where we left of after clicking Donate.
    >>> browser.open(saved_url)
    >>> browser.getControl('Your Name').value = 'Test'
    >>> browser.getControl('Phone Number').value = '1234567'
    >>> browser.getControl('Phone Number').value = '12345678'
    >>> browser.getControl(name='form.email').value = 'test@test.com'
    >>> browser.getControl(name='form.bill_name').value = 'Test'
    >>> browser.getControl(name='form.bill_first_line').value = 'Test'
    >>> browser.getControl(name='form.bill_city').value = 'Test'
    >>> browser.getControl(name='form.bill_state').value = ('US-HI',)
    >>> browser.getControl(name='form.bill_postal_code').value = '12345'
    >>> browser.getControl(name='form.ship_first_line').value = 'Test'
    >>> browser.getControl(name='form.ship_city').value = 'Test'
    >>> browser.getControl(name='form.ship_state').value = ('US-HI',)
    >>> browser.getControl(name='form.ship_postal_code').value = '12345'

Now go to the next form.
    >>> try:
    ...     browser.getControl('Continue').click()
    ... except:
    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
    ...     import pdb; pdb.set_trace()

#    >>> browser.getControl(name="form.payment_processor").value = ['Luottokunta Processor']
#    >>> try:
#    ...     browser.getControl(name="form.actions.continue").click()
#    ... except:
#    ...     print self.portal.error_log.getLogEntries()[0]['tb_text']
#    ...     import pdb; pdb.set_trace()

    >>> order_id = browser.getControl(name="Order_ID").value
    >>> state = "REVIEWING"
    >>> thanks_url = "http://nohost/plone/@@luottokunta-thank-you?order_id=%s&amp;finance_state=%s" %(order_id, state)
    >>> ("value=\"%s\"" %(thanks_url)) in browser.contents
    False
    >>> "id=\"Authentication_Mac\"" in browser.contents
    True
    >>> ("value=\"%s\"" %(order_id)) in browser.contents
    True
    >>> "value=\"3300\"" in browser.contents
    True
