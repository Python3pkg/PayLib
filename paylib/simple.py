from paylib.paypal import core, fields

from paylib.paypal.requests import createrecurringpaymentsprofile as createrecurring
from paylib.paypal.requests import managerecurringpaymentsprofilestatus as managerecurring
from paylib.paypal.requests import setexpresscheckout as setexpress

from paylib import static

from datetime import datetime

class Transaction(object):
    """
    Simplified abstraction for a PayPal Express Checkout NVP API transaction
    """
    
    LIVE_URL = 'https://www.paypal.com/webscr?cmd=%s&token='
    TEST_URL = 'https://www.sandbox.paypal.com/webscr?cmd=%s&token='
    
    CMD_EXPRESS_CHECKOUT = '_express-checkout'
    
    BILLING_PERIOD = ['Day', 'Week', 'SemiMonth', 'Month', 'Year']
    
    def __init__(self, user, passwd, sig, live):
        """
        Initialise PayPal object mandatory attributes
        
        """
        self.user = core.BaseProfile(
            username=user,
            password=passwd)
        self.user.set_signature(sig)
        
        self.live = live
        if live:
            self.url = Transaction.LIVE_URL
        else:
            self.url = Transaction.TEST_URL
        self.ccy = None
        self.uid = None
        self.token = None
        self.amount = None
        self.digital = None
        self.description = None
        

class Subscription(Transaction):
    
    def start(self, amount, ccy, desc,
                success_callback, fail_callback, 
                digital=True):
        """
        Generates the PayPal url the user should be redirected to. 
        Calls SetExpressCheckout to create the initial payment.
        
        amount: Float in format d.dd
        ccy: Three letter currency code. See static.currency_set
        desc: Product description,
        success_callback: Url PayPal redirects to on completion
        fail_callback: Url PayPal redirects to if transaction is stopped.
        digital: Whether product is physical or digital goods.
        
        Returns PayPal url customer should be redirected to.
        """
        ec_url = self.url % Transaction.CMD_EXPRESS_CHECKOUT
        # create payment
        payment = fields.Payment()
        if ccy not in static.currency_set:
            raise ValueError('Invalid period argument: %s' % ccy)
        else:
            self.ccy = ccy
        payment.set_currency(self.ccy)
        self.amount = str(amount)
        payment.set_amount(self.amount)

        # create SetExpressCheckout - 1st paypal request
        set_ec = setexpress.SetExpressCheckout(
            payment, success_callback,
            fail_callback)

        ba = fields.BillingAgreement()
        ba.set_billing_type('RecurringPayments')
        self.description = desc
        ba.set_description(self.description)
        
        set_ec.set_billing_agreement([ba])
        self.digital = digital
        if digital:
            set_ec.set_require_confirmed_shipping(False)
            set_ec.set_no_shipping(True)
        else:
            set_ec.set_require_confirmed_shipping(True)
            set_ec.set_no_shipping(False)
        
        set_ec.set_max_amount(amount)

        paypal = core.PayPal(self.user, sandbox = not self.live)
        paypal.set_response(set_ec)

        # get nvp response

        response = set_ec.get_nvp_response()

        self.token = response['TOKEN']

        # send the user to PayPal using following url
        redirect_url = ec_url+self.token
        
        return redirect_url

    def finish(self, email, name, period, freq, qty=1):
        """
        Callback function to be executed when user PayPal process completes.
        Calls CreateRecurringPaymentsProfile to create the subscription. 
        Place this in callback handler to initiate the recurring payment 
        once the user returns from paypal.
        
        email: Customer email.
        name: Name of subscription.
        period: Billing. One of Transaction.BILLING_PERIOD list.
        freq: Billing frequency. Int value that when multiplied by 
        period cannot exceed one year.
        qty: Number of subs being purchased.
        """
        # N.B. ScheduleDetails description must be exact match of BillingAgreement's description in call to SetExpressCheckout above!
        schedule_details = fields.ScheduleDetails(self.description)

        sub = fields.PaymentItem()
        if self.digital:
            sub.set_category('Digital')
        else:
            sub.set_category('Physical')
        sub.set_name(name)
        sub.set_description(self.description)
        sub.set_amount(self.amount)
        sub.set_quantity(qty)

        # create payment
        payment = fields.Payment(items=[sub])        

        create_recurring = createrecurring.CreateRecurringPaymentsProfile( self.token, payment, schedule_details)

        profile_details = fields.RecurringPaymentsProfileDetails(datetime.now())
        create_recurring.set_recurring_payments_profile_details(profile_details)
        
        if period not in Transaction.BILLING_PERIOD:
            raise ValueError('Invalid period argument: %s' % period)        
        billing_period_details = fields.BillingPeriodDetails(period,freq,self.amount,self.ccy)
        create_recurring.set_billing_period_details(billing_period_details)

        payer_information = fields.PayerInformation()
        payer_information.set_email(email)
        create_recurring.set_payer_information(payer_information)

        paypal = core.PayPal(self.user, sandbox = not self.live)
        paypal.set_response(create_recurring)

        # get nvp response
        response = create_recurring.get_nvp_response()

        self.uid = response['PROFILEID'] # store for recurring payment management later

    def cancel(self):
        """
        Cancel an active subscription
        """
        paypal = core.PayPal(self.user, sandbox= not self.live)
        manage_recurring = managerecurring.ManageRecurringPaymentsProfileStatus( self.uid, 'Cancel', 'Cancelling Subscription')
        paypal.set_response(manage_recurring)

        response = manage_recurring.get_nvp_response()        
