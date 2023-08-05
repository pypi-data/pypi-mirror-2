from decimal import Decimal
from zope.interface import implements
from zope.component import adapts, getUtility
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
try:
    # For Plone-4
    import hashlib
except:
    # For Plone-3
    import md5

from zope.app.component.hooks import getSite
from getpaid.core.order import Order

### For implements.
from getpaid.luottokunta.interfaces import ILuottokuntaOrderInfo

### For call.
from getpaid.luottokunta.interfaces import (
    IDecimalPrice,
    ILuottokuntaOptions,
    ILuottokuntaLanguage,
)

class LuottokuntaOrderInfo(object):

    implements(ILuottokuntaOrderInfo)
    adapts(Order)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Returns information of order."""
        site = getSite()
        context = aq_inner(self.context)
        membership = getToolByName(site, 'portal_membership')
        member_id = membership.getAuthenticatedMember().getId()
        getpaid_order_id = context.order_id
        customer_id = getpaid_order_id
        ## Because Luottokunta allows only 12 characters for customer_id...
        customer_id = customer_id[:12]
        dp = getUtility(IDecimalPrice)
        price = dp(context.getTotalPrice())
        luottokunta_price = unicode(Decimal(price * 100).quantize(Decimal('1')))
        options = ILuottokuntaOptions(site)
        merchant_number = options.merchant_number
        if options.use_incremental_order_id and options.next_order_id:
            order_id = str(options.next_order_id)
        else:
            order_id = getpaid_order_id
        if options.use_dossier_id:
            dossier_id = options.dossier_id
        else:
            dossier_id = None
        if options.card_details_transmit:
            card_details_transmit = "1"
            language = None
        else:
            card_details_transmit = "0"
            language_tool = getToolByName(site, "portal_languages")
            language_bindings = language_tool.getLanguageBindings()
            luottokunta_language = getUtility(ILuottokuntaLanguage)
            language = luottokunta_language(language_bindings)
        if options.transaction_type:
            transaction_type = "1"
        else:
            transaction_type = "0"
        if options.use_authentication_mac and options.authentication_mac:
            try:
                m = hashlib.md5()
            except:
                m = md5.new()
            m.update(merchant_number)
            m.update(order_id)
            m.update(luottokunta_price)
            m.update(transaction_type)
            m.update(options.authentication_mac)
            authentication_mac = m.hexdigest()
        else:
            authentication_mac = None
        base_url = site.absolute_url()
        success_url = base_url + '/@@luottokunta-thank-you?getpaid_order_id=%s&luottokunta_order_id=%s' %(getpaid_order_id, order_id)
        failure_url = base_url + '/@@luottokunta-declined?getpaid_order_id=%s&luottokunta_order_id=%s' %(getpaid_order_id, order_id)
        cancel_url = base_url + '/@@luottokunta-cancelled?getpaid_order_id=%s&luottokunta_order_id=%s' %(getpaid_order_id, order_id)
        order_info = {
                        'merchant_number' : merchant_number,
                        'price' : luottokunta_price,
                        'authentication_mac' : authentication_mac,
                        'order_number' : order_id,
                        'getpaid_order_id': getpaid_order_id,
                        'card_details_transmit' : card_details_transmit,
                        'transaction_type' : transaction_type,
                        'success_url' : success_url,
                        'failure_url' : failure_url,
                        'cancel_url' : cancel_url,
                        'language' : language,
                        'customer_id' : customer_id,
        }
        return order_info
