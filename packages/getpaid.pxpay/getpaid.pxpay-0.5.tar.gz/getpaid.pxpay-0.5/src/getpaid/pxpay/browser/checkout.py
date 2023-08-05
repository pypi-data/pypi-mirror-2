import decimal,operator
from exceptions import Exception

from zope import component
from zope import schema
from zope.formlib import form
from zc.table import column

from getpaid.core import interfaces, options
from getpaid.wizard import interfaces as wizard_interfaces
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay, \
     sanitize_custom_widgets, null_condition
from Products.PloneGetPaid.browser import cart as cart_core
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions

from getpaid.pxpay.interfaces import IPXPayPaymentProcessor
from getpaid.pxpay.exceptions import PXPayException

from Products.PloneGetPaid.i18n import _

class PxPayCheckoutReviewAndPay( CheckoutReviewAndPay ):
    """
    Override the default PloneGetPaid CheckoutReviewAndPay step so
    that we can handle the details of the pxpay async processing of
    credit card details.
    """
    sections = ()

    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

    columns = [
        column.GetterColumn( title=_(u"Quantity"), getter=cart_core.LineItemColumn("quantity") ),
        column.GetterColumn( title=_(u"Name"), getter=cart_core.lineItemURL ),
        column.GetterColumn( title=_(u"Price"), getter=cart_core.lineItemPrice ),
        column.GetterColumn( title=_(u"Total"), getter=cart_core.lineItemTotal ),
       ]

    def customise_widgets(self,fields):
        pass

    def getSchemaAdapters( self ):
        return []

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}

        # grab all the adapters and fields from the entire wizard form
        # sequence (till the current step)
        adapters = self.wizard.data_manager.adapters
        fields   = self.wizard.data_manager.fields

        # display widgets for bill/ship address
        bill_ship_fields = []
        form_schemas = component.getUtility(
            interfaces.IFormSchemas)
        for i in (form_schemas.getInterface('billing_address'),
                  form_schemas.getInterface('shipping_address')):
            bill_ship_fields.append(fields.select(*schema.getFieldNamesInOrder(i)))
        # make copies of custom widgets.. (typically for edit, we want display)
        bill_ship_fields = sanitize_custom_widgets(
            reduce(operator.__add__,bill_ship_fields)
            )

        self.widgets = form.setUpEditWidgets(
            bill_ship_fields,  self.prefix, self.context, self.request,
            adapters=adapters, for_display=True, ignore_request=ignore_request
            )

    @form.action(_(u"Cancel"), name="cancel", validator=null_condition )
    def handle_cancel( self, action, data):
        url = self.context.portal_url.getPortalObject().absolute_url()
        url = url.replace("https://", "http://")
        return self.request.response.redirect(url)

    @form.action(_(u"Back"), name="back", validator=null_condition )
    def handle_back( self, action, data):
        self.next_step_name = wizard_interfaces.WIZARD_PREVIOUS_STEP

    @form.action(_(u"Make Payment"), name="make-payment" )
    def makePayment( self, action, data ):
        """ create an order, and submit to the pxpay processor """
        portal = self.context.portal_url.getPortalObject()
        manage_options = IGetPaidManagementOptions( portal )
        processor_name = manage_options.payment_processor
        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )
        processor = component.getAdapter( portal,
                                          interfaces.IPaymentProcessor,
                                          processor_name )
        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        order_manager = component.getUtility( interfaces.IOrderManager )
        order_manager.store( order )
        # the following will redirect to the pxpay web interface to
        # capture creditcard details
        if IPXPayPaymentProcessor.providedBy(processor):
            processor.authorize( order, None, self.request )
        else:
            raise PXPayException("This checkout implementation requires the PXPay payment processor.")

