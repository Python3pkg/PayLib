PayLib is your easy python payments API for PayPal.

It is based on the great work of Luca Sepe's [PyPal-NVP](http://code.google.com/p/pypal-nvp/) which is itself based on a java implementation over at [sourceforge](http://sourceforge.net/projects/paypal-nvp/).

The underlying engine has been updated to reflect more recent changes in the PayPal Name Value Pair (NVP) API and extended to offer a more complete coverage of the Express Checkout API methods. I'm also partially using it to become a better Python programmer hopefully by evolving it's codebase into a more pythonic implementation over time.

For now you can set up & manage PayPal subscriptions using PayLib quickly and cleanly with minimal code, giving you an easy way of earning regular payments for your web app. The first site to take advantage of PayLib is [One Click Analytics](http://www.oneclickanalytics.com/).

Usage:
======

To create a recurring payment (subscription):
---------------------------------------------

How to setup a recurring payment with your customer for $10 a year.

```python
from paylib import simple

user = '<your paypal username>'
passwd = '<your paypal password>'
sig = '<your paypal signature>'
live = False # run against PayPal sandbox

sub = simple.Subscription( user, passwd, sig, live)

amount = '10.00'
ccy = 'USD'
desc = 'My Annual Super Duper Subscription'
success_callback = 'https://your-site.com/paypal_success'
fail_callback = 'https://your-site.com/paypal_fail'

redir = sub.start( amount, ccy, desc, success_callback, fail_callback)

# store the subscription object somewhere 
# (hint: you should have a customer obj but sub.token is unique) 
# forward the user to paypal servers to complete the transaction
self.redirect(redir)
```

```python
# in your success_callback url handler you recall the subscription object & create the recurring payment
email = 'customer@example.com'
name = 'Super Duper Annual Subscription'
period = 'Year'
freq = 1

sub.finish( email, name, period, freq)
```

```python
# cancel a subscription

sub.cancel()
```

Integrating with PayLib
-----------------------

I've written an overview showing how easy it is to create a web application earning money via PayLib from the start with zero startup costs in [the 60 minute web app](http://aleatory.clientsideweb.net/2012/10/26/60-minute-web-app)

License
-------

PayLib is released under the MIT License

Copyright (C) 2013 Client Side Web

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
