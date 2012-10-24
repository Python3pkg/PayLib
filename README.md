PayLib is your easy python payments API for PayPal and, in future, Google Wallet.

It is based on the great work of Luca Sepe’s [PyPal-NVP](http://code.google.com/p/pypal-nvp/) which is itself based on a java implementation over at [sourceforge](http://sourceforge.net/projects/paypal-nvp/).

PayLib is updated to reflect more recent changes in the PayPal Name Value Pair (NVP) API and extended to offer a more complete coverage of the Express Checkout API methods. I’m also partially using it to become a better Python programmer hopefully by evolving it’s codebase into a more pythonic implementation over time.

For now you can set up & manage digital subscriptions using PayLib quickly and cleanly, giving you an easy way of earning regular payments for your web app. The first site to take advantage of PayLib is One Click Analytics.

Usage:
======

To create a recurring payment (subscription):
---------------------------------------------

How to setup a recurring payment with your customer for $10 a year.

```python
# universal settings

import csw.ecommerce.paypal.core
import csw.ecommerce.paypal.requests.setexpresscheckout
import csw.ecommerce.paypal.requests.createrecurringpaymentsprofile
import csw.ecommerce.paypal.requests.managerecurringpaymentsprofilestatus
import csw.ecommerce.paypal.requests.doexpresscheckoutpayment
import csw.ecommerce.paypal.fields

paypal_settings = {'user':'<your username here>','passwd':'<your password here>','sig':'<your signature here>','express_checkout':'https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=','product_desc':'Super Duper Machine v1'}

paypal_user = csw.ecommerce.paypal.core.BaseProfile(
	username=paypal_settings['user'],
	password=paypal_settings['passwd'])
paypal_user.set_signature(settings['sig'])
```

```python
# initial call to SetExpressCheckout

# create payment
payment = csw.ecommerce.paypal.fields.Payment()
payment.set_currency('USD')
payment.set_amount('10.00')

# create SetExpressCheckout - 1st paypal request
set_ec = csw.ecommerce.paypal.requests.setexpresscheckout.SetExpressCheckout(
	payment, '<your success callback url>',
	'<your cancelled callback url>')

ba = csw.ecommerce.paypal.fields.BillingAgreement()
ba.set_billing_type('RecurringPayments')
ba.set_description(paypal_settings['product_desc'])

set_ec.set_billing_agreement([ba])
set_ec.set_require_confirmed_shipping(False)
set_ec.set_no_shipping(False)
set_ec.set_max_amount('10.00')

paypal = csw.ecommerce.paypal.core.PayPal(paypal_user)
paypal.set_response(set_ec)

# get nvp response

response = set_ec.get_nvp_response()

token = response['TOKEN']

# send the user to PayPal using following url
redirect_url = settings['express_checkout']+token
```

```python
# create the recurring payment
# place this in your callback handler to initiate the recurring payment once the user returns from paypal

# N.B. ScheduleDetails description must be exact match of BillingAgreement's description in call to SetExpressCheckout above!
schedule_details = csw.ecommerce.paypal.fields.ScheduleDetails(paypal_settings['product_desc'])

sub = csw.ecommerce.paypal.fields.PaymentItem()
sub.set_category('Digital')
sub.set_name('Subscription')
sub.set_description('Paid account')
sub.set_amount('10.00')
sub.set_quantity(1)

# create payment
payment = csw.ecommerce.paypal.fields.Payment(items=[sub])		

create_recurring = csw.ecommerce.paypal.requests.createrecurringpaymentsprofile.CreateRecurringPaymentsProfile(token, payment, schedule_details)

profile_details = csw.ecommerce.paypal.fields.RecurringPaymentsProfileDetails(datetime.now())
create_recurring.set_recurring_payments_profile_details(profile_details)

period = 'Day'
billing_period_details = csw.ecommerce.paypal.fields.BillingPeriodDetails(period,1,'10.00','USD')
create_recurring.set_billing_period_details(billing_period_details)

payer_information = csw.ecommerce.paypal.fields.PayerInformation()
payer_information.set_email(<user email address>)
create_recurring.set_payer_information(payer_information)

paypal = csw.ecommerce.paypal.core.PayPal(paypal_user)
paypal.set_response(create_recurring)

# get nvp response
response = create_recurring.get_nvp_response()

profile_id = response['PROFILEID'] # store for recurring payment management later
```

```python
# cancel a subscription

paypal = csw.ecommerce.paypal.core.PayPal(paypal_user)
manage_recurring = csw.ecommerce.paypal.requests.managerecurringpaymentsprofilestatus.ManageRecurringPaymentsProfileStatus(profile_id,'Cancel','Cancelling Subscription')
paypal.set_response(manage_recurring)

response = manage_recurring.get_nvp_response()
```

Integrating with PayLib
-----------------------

I've written an overview showing how easy it is to create a web application earning money from the start with no outlay from yourself in [the 60 minute web app](http://aleatory.clientsideweb.net/2012/10/26/60-minute-web-app)