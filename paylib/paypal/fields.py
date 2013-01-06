# Copyright (C) 2011 Luca Sepe <luca.sepe@gmail.com>
# updates to support Paypal API v.86 (C) 2012 Client Side Web <rutherford@clientsideweb.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import abc
import StringIO
import copy

from paylib import static

from paylib.paypal import util

class RequestFields( object ):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_nvp_request( self ):    
        """Creates and returns part of the NVP (name value pair) request containing request values."""


class Address( RequestFields ):

    def __init__( self, street, city, state, country='IT' ):
        self._nvp_request = dict()
        self._nvp_request['STREET'] = street
        self._nvp_request['CITY'] = city
        self._nvp_request['STATE'] = state
        self._nvp_request['COUNTRY'] = country

    def set_street_2( self, street):
        """Second street address.
        Character length and limitations: 100 single-byte characters."""
        if len(street) > 100:
            raise ValueError( 'street can be maximum 100 characters.' )
        self._nvp_request['STREET2'] = street


    def set_zip( self, zip_code ):
        """U.S. ZIP code or other country-specific postal code. 
        Required if using a U.S. shipping address may be required for other countries.  
        Character length and limitations: 20 single-byte characters."""
        if len(zip_code) > 20:
            raise ValueError( 'zip_code can be maximum 20 characters.' )
        self._nvp_request['ZIP'] = zip_code


    def set_phone_number( self, phone_number ):
        """Phone number. Character length and limit: 20 single-byte characters."""
        if len(phone_number) > 20:
            raise ValueError( 'phone_number can be maximum 20 characters.' )
        self._nvp_request['SHIPTOPHONENUM'] = phone_number

    def get_nvp_request( self ):
        return self._nvp_request
    



class ShipToAddress( RequestFields ):

    def __init__( self, name, street, city, state, country='IT' ):
        """name is the Person's name associated with this shipping address (max 32 single-byte chars)
        street is the First street address (max 100 single-byte characters).
        city is the Name of city (max 40 single-byte characters).
        state is the State or province (max 40 single-byte character).
        country is the Country code."""
        if (len(name) > 32) or (len(street) > 100) or (len(city) > 40) or (len(state) > 40):
            raise ValueError( 'Characters limit exceeded.' )

        self._nvp_request = dict()
        self._nvp_request['SHIPTONAME'] = name
        self._nvp_request['SHIPTOSTREET'] = street
        self._nvp_request['SHIPTOCITY'] = city
        self._nvp_request['SHIPTOSTATE'] = state
        self._nvp_request['SHIPTOCOUNTRY'] = country

    def set_street_2( self, street):
        """Second street address.
        Character length and limitations: 100 single-byte characters."""
        if len(street) > 100:
            raise ValueError( 'street can be maximum 100 characters.' )
        self._nvp_request['SHIPTOSTREET2'] = street


    def set_zip( self, zip_code ):
        """U.S. ZIP code or other country-specific postal code. 
        Required if using a U.S. shipping address may be required for other countries.  
        Character length and limitations: 20 single-byte characters."""
        if len(zip_code) > 20:
            raise ValueError( 'zip_code can be maximum 20 characters.' )
        self._nvp_request['SHIPTOZIP'] = zip_code


    def set_phone_number( self, phone_number ):
        """Phone number. Character length and limit: 20 single-byte characters."""
        if len(phone_number) > 20:
            raise ValueError( 'phone_number can be maximum 20 characters.' )
        self._nvp_request['SHIPTOPHONENUM'] = phone_number

    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    




class ShippingOptions( RequestFields ):

    def __init__( self ):
        self._nvp_request = dict()

    def set_default_shipping_option( self, is_default ):
        """Required if specifying the Callback URL.
        When the value of this flat rate shipping option is true, PayPal 
        selects it by default for the buyer and reflects it in the "default" total.
        
        Note:
        There must be ONE and ONLY ONE default. It is not OK to have no default."""
        option = 'true' if is_default else 'false'
        self._nvp_request['L_SHIPPINGOPTIONISDEFAULT'] = option


    def set_shipping_name( self, name ):
        """Required if specifying the Callback URL.
        The internal name of the shipping option such as Air, Ground, 
        Expedited, and so forth. 

        Character length and limitations: 50 character-string."""

        if len(name) > 50:
            raise ValueError( 'name can be maximum 50 characters.' )
        self._nvp_request['L_SHIPPINGOPTIONNAME'] = name


    def set_shipping_label( self, label ):
        """Required if specifying the Callback URL. 
        The label for the shipping option as displayed to the user. 
        Examples include: Air: Next Day, Expedited: 3-5 days, Ground: 5-7 days, 
        and so forth. Shipping option labels can be localized based on the 
        buyer's locale, which PayPal sends to your website as a parameter value 
        in the callback request. 

        Character length and limitations: 50 character-string."""
        if len(label) > 50:
            raise ValueError( 'label can be maximum 50 characters.' )
        self._nvp_request['L_SHIPPINGOPTIONLABEL'] = label
    

    def set_shipping_amount( self, amount ):
        """Required if specifying the Callback URL. 
        The amount of the flat rate shipping option. 

        Limitations: 

            - Must not exceed $10,000 USD in any currency.
            - No currency symbol.
            - Must have two decimal places, decimal separator must be a period (.)."""
        
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            sb = StringIO.StringIO()
            sb.write( 'Amount {0} is not valid. '.format(amount) )
            sb.write( 'Amount has to have exactly two decimal ' )
            sb.write( 'places seaprated by \".\" ' )
            sb.write( '- example: \"50.00\"' )
            raise ValueError( sb.getvalue() )
        
        self._nvp_request['L_SHIPPINGOPTIONAMOUNT'] = amount


    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)



class BillingAgreement( RequestFields ):

    def __init__( self ):
        self._nvp_request = dict()
        

    def set_billing_type( self, billing_type ):
        """Type of billing agreement.
        For recurring payments, this field must be set to 'RecurringPayments'
        and description (set_description) MUST be set as well.
        In this case, you can specify up to ten billing agreements. 
        
        Note: Other defined values are not valid."""
        self._nvp_request['L_BILLINGTYPE'] = billing_type

    def set_description( self, description ):
        """Description of goods or services associated with the billing agreement, 
        which is required for each recurring payment billing agreement.
        PayPal recommends that the description contain a brief summary of the 
        billing agreement terms and conditions.
        For example, customer will be billed at "9.99 per month for 2 years".
        
        Character length and limitations: 127 single-byte alphanumeric bytes."""
        if len(description) > 127:
            raise ValueError( 'description can be maximum 127 characters.' )
        self._nvp_request['L_BILLINGAGREEMENTDESCRIPTION'] = description 

    def set_payment_type( self, payment_type ):
        """Type of PayPal payment you require for the 
        billing agreement ('Any' or 'InstantOnly').
        
        Note: For recurring payments, this field is ignored."""
        if payment_type not in ['Any', 'InstantOnly']:
            raise ValueError( 'payment_type must be Any or InstantOnly' )
        self._nvp_request['L_PAYMENTTYPE'] = payment_type 

    def set_custom_field( self, field ):
        """Custom annotation field for your own use.
        
        Note: For recurring payments, this field is ignored.
        
        Character length and limitations: 256 single-byte alphanumeric bytes."""
        if len(field) > 256:
            raise ValueError( 'description can be maximum 256 characters.' )
        self._nvp_request['L_BILLINGAGREEMENTCUSTOM'] = field 

    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)

# DO NOT USE. For deletion.
class BillingAgreementMulti( RequestFields ):
    
    BILLING_TYPE = set(['RecurringPayments','MerchantInitiatedBilling','MerchantInitiatedBillingSingleAgreement'])
    PAYMENT_TYPE = set(['Any','InstantOnly'])
    
    def __init__( self ):
        self._nvp_request = dict()
        

    def set_billing_type( self, bill_type, payment_number ):
        """Type of billing agreement.
        For recurring payments, this field must be set to 'RecurringPayments'
        and description (set_description) MUST be set as well.
        In this case, you can specify up to ten billing agreements. 
        
        Note: Other defined values are not valid."""
        if bill_type not in BillingAgreementMulti.BILLING_TYPE:
            raise ValueError('bill_type must be in BillingAgreementMulti.BILLING_TYPE')
        
        self._nvp_request[('L_BILLINGTYPE%d' % payment_number)] = BillingAgreementMulti.BILLING_TYPE[bill_type]
        
    def set_ref_billing_type(self, bill_type):
        """Type of billing agreement for reference transactions. 
        You must have permission from PayPal to use this field."""
        if bill_type not in BillingAgreementMulti.BILLING_TYPE:
            raise ValueError('bill_type must be in BillingAgreementMulti.BILLING_TYPE')
        
        self._nvp_request['BILLINGTYPE'] = BillingAgreementMulti.BILLING_TYPE[bill_type]

    def set_description( self, description, payment_number ):
        """Description of goods or services associated with the billing agreement, 
        which is required for each recurring payment billing agreement.
        PayPal recommends that the description contain a brief summary of the 
        billing agreement terms and conditions.
        For example, customer will be billed at "9.99 per month for 2 years".
        
        Character length and limitations: 127 single-byte alphanumeric bytes."""
        if len(description) > 127:
            raise ValueError( 'description can be maximum 127 characters.' )
        self._nvp_request[('L_BILLINGAGREEMENTDESCRIPTION%d' % payment_number)] = description 

    def set_payment_type( self, pay_type, payment_number ):
        """(Optional) Type of PayPal payment you 
        require for the billing agreement.
        
        Note: For recurring payments, this field is ignored."""
        if pay_type not in BillingAgreementMulti.PAYMENT_TYPE:
            raise ValueError( 'pay_type must be in BillingAgreementMulti.PAYMENT_TYPE' )
        self._nvp_request[('L_PAYMENTTYPE%d' % payment_number)] = BillingAgreementMulti.PAYMENT_TYPE[pay_type]

    def set_custom_field( self, field, payment_number ):
        """(Optional) Custom annotation field for your own use.
        
        Note: For recurring payments, this field is ignored.
        
        Character length and limitations: 256 single-byte alphanumeric bytes."""
        if len(field) > 256:
            raise ValueError( 'description can be maximum 256 characters.' )
        self._nvp_request[('L_BILLINGAGREEMENTCUSTOM%d' % payment_number)] = field 

    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)

# naive of payment, item numbers until PaymentMulti does the job
class PaymentItem( RequestFields ):

    """Payment Details Item Type Fields. 
    You have to set amount for at leas one item.
    Otherwise the payment will be rejected by paypal, because order will be 0.00
    
    You can specify up to 10 payments, where n is a digit between 0 and 9, inclusive, 
    and m specifies the list item within the payment except for digital goods, 
    which supports single payments only. These parameters must be ordered sequentially 
    beginning with 0 (for example L_PAYMENTREQUEST_n_NAME0, L_PAYMENTREQUEST_n_NAME1)."""
    
    ITEM_CATEGORY = set(['Digital','Physical'])
    
    def __init__( self ):
        self._nvp_request = dict()
    
    def set_category(self, category):
        """Indicates whether the item is digital or physical. For digital goods, 
        this field is required and must be set to Digital to get the best rates."""
        if category not in PaymentItem.ITEM_CATEGORY:
            raise ValueError('Category must be a member of PaymentItem.ITEM_CATEGORY set')
        
        self._nvp_request['L_PAYMENTREQUEST_%d_NAME%d'] = category

    def set_name( self, name ):
        """Item name. Character length and limitations: 127 single-byte characters."""
        if len( name ) > 127:
            raise ValueError( 'Name cannot exceed 127 characters' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_NAME%d'] = name


    def set_description( self, description ):
        """(Optional) Item description. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies 
        the list item within the payment except for digital goods, 
        which supports single payments only. These parameters must be 
        ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_DESC0, L_PAYMENTREQUEST_n_DESC1)."""
        
        if len( description ) > 127:
            raise ValueError( 'Name cannot exceed 127 characters' )
            
        self._nvp_request['L_PAYMENTREQUEST_%d_DESC%d'] = description


    def set_amount( self, amount ):
        """Cost of item. This field is required when 
        L_PAYMENTREQUEST_n_ITEMCATEGORYm is passed.You can specify 
        up to 10 payments, where n is a digit between 0 and 9, 
        inclusive, and m specifies the list item within the payment 
        except for digital goods, which supports single payments only. 
        These parameters must be ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_AMT0, L_PAYMENTREQUEST_n_AMT1).
        
        NOTE:If you specify a value for L_PAYMENTREQUEST_n_AMTm , 
        you must specify a value for PAYMENTREQUEST_n_ITEMAMT.
        
        Character length and limitations: Value is a positive number 
        which cannot exceed $10,000 USD in any currency. It includes 
        no currency symbol. It must have 2 decimal places, the decimal 
        separator must be a period (.), and the optional thousands 
        separator must be a comma (,)."""
        
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            sb = StringIO.StringIO()
            sb.write( 'Amount {0} is not valid. '.format(amount) )
            sb.write( 'Amount has to have exactly two decimal ' )
            sb.write( 'places seaprated by \".\" ' )
            sb.write( '- example: \"50.00\"' )
            raise ValueError( sb.getvalue() )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_AMT%d'] = amount


    def set_item_number( self, item_number ):
        """(Optional) Item number. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies 
        the list item within the payment. These parameters must be 
        ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_NUMBER0, L_PAYMENTREQUEST_n_NUMBER1)."""
        
        if len( item_number ) > 127:
            raise ValueError( 'Item number cannot exceed 127 characters' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_NUMBER%d'] = item_number


    def set_quantity( self, quantity ):
        """Item quantity. This field is required when L_PAYMENTREQUEST_n_ITEMCATEGORYm 
        is passed. For digital goods (L_PAYMENTREQUEST_n_ITEMCATEGORYm=Digital), 
        this field is required. You can specify up to 10 payments, where n is 
        a digit between 0 and 9, inclusive, and m specifies the list item 
        within the payment except for digital goods, which only supports 
        single payments. These parameters must be ordered sequentially 
        beginning with 0 
        (for example L_PAYMENTREQUEST_n_QTY0, L_PAYMENTREQUEST_n_QTY1)."""
        quantity = int( quantity )
        if quantity < 0:
            raise ValueError( 'Quantity has to be positive integer' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_QTY%d'] = '{0}'.format(quantity)

                
    def set_tax_amount( self, amount ):
        """(Optional) Item sales tax. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies 
        the list item within the payment except for digital goods, 
        which only supports single payments. These parameters must be 
        ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_TAXAMT0, L_PAYMENTREQUEST_n_TAXAMT1)."""
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            sb = StringIO.StringIO()
            sb.write( 'Amount {0} is not valid. '.format(amount) )
            sb.write( 'Amount has to have exactly two decimal ' )
            sb.write( 'places seaprated by \".\" ' )
            sb.write( '- example: \"50.00\"' )
            raise ValueError( sb.getvalue() )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_TAXAMT%d'] = amount


    def set_weight( self, value, unit ):
        """(Optional) Item weight corresponds to the weight of the item. 
        You can pass this data to the shipping carrier as is without having 
        to make an additional database query. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies the 
        list item within the payment. These parameters must be ordered 
        sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_ITEMWEIGHTVALUE0, L_PAYMENTREQUEST_n_ITEMWEIGHTVALUE1)."""
        val = int(value)
        if val < 0:
            raise ValueError( 'Value has to be positive integer' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMWEIGHTVALUE%d']= '{0}'.format( val )
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMWEGHTUNIT%d'] = unit

    
    def set_length( self, value, unit ):
        """(Optional) Item length corresponds to the length of the item. 
        You can pass this data to the shipping carrier as is without having 
        to make an additional database query. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies the 
        list item within the payment. These parameters must be ordered 
        sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_ITEMLENGTHVALUE0, L_PAYMENTREQUEST_n_ITEMLENGTHVALUE1)."""

        val = int(value)
        if val < 0:
            raise ValueError( 'Value has to be positive integer' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMLENGTHVALUE%d'] = '{0}'.format( val )
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMLENGTHUNIT%d'] = unit


    def set_width( self, value, unit ):
        """(Optional) Item width corresponds to the width of the item. 
        You can pass this data to the shipping carrier as is without 
        having to make an additional database query. You can specify 
        up to 10 payments, where n is a digit between 0 and 9, inclusive, 
        and m specifies the list item within the payment. 
        These parameters must be ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_ITEMWIDTHVALUE0, L_PAYMENTREQUEST_n_ITEMWIDTHVALUE1)."""

        val = int(value)
        if val < 0:
            raise ValueError( 'Value has to be positive integer' )
        
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMWIDTHVALUE'] = '{0}'.format( val )
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMWIDTHUNIT'] = unit


    def set_height( self, value, unit ):
        """(Optional) Item height corresponds to the height of the item. 
        You can pass this data to the shipping carrier as is without 
        having to make an additional database query. You can specify 
        up to 10 payments, where n is a digit between 0 and 9, inclusive, 
        and m specifies the list item within the payment. 
        These parameters must be ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_ITEMHEIGHTVALUE0, L_PAYMENTREQUEST_n_ITEMHEIGHTVALUE1)."""

        val = int(value)
        if val < 0:
            raise ValueError( 'Value has to be positive integer' )

        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMHEIGHTVALUE'] = '{0}'.format( val )
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMHEIGHTUNIT'] = unit

    def set_item_url(self, value):
        """(Optional) URL for the item. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive, and m specifies 
        the list item within the payment. These parameters must be 
        ordered sequentially beginning with 0 (for example 
        L_PAYMENTREQUEST_n_ITEMURL0, L_PAYMENTREQUEST_n_ITEMURL1)."""
        # TODO: need url validator here
        val = value
        
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMURL%d'] = val
    
    def set_item_category(self, value):
        """Indicates whether an item is digital or physical. For digital goods, 
        this field is required and must be set to Digital. You can specify 
        up to 10 payments, where n is a digit between 0 and 9, inclusive, 
        and m specifies the list item within the payment 
        except for digital goods, which only supports single payments. 
        These parameters must be ordered sequentially beginning with 0 
        (for example L_PAYMENTREQUEST_n_ITEMCATEGORY0, L_PAYMENTREQUEST_n_ITEMCATEGORY1)."""
        val = value
        if val not in PaymentItem.ITEM_CATEGORY:
            raise ValueError('Invalid item category')
        
        self._nvp_request['L_PAYMENTREQUEST_%d_ITEMCATEGORY%d'] = PaymentItem.ITEM_CATEGORY[val]
        
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)


    def __str__( self ):
        sb = StringIO.StringIO()
        sb.write( 'instance of PaymentDetailsItem class with ' )
        sb.write( 'the nvpRequest values: ' )
        sb.write( str(self._nvp_request) )
        return sb.getvalue()

    def __del__( self ):
        del (self._nvp_request)

class Payment( RequestFields ):

    """Payment Details Type Fields. 
    For simple payments use constructor with amount field. 
    If you want to set tax, or more options, use Constructor that takes PaymentItem list."""

    PAYMENT_ACTION = set(['Sale','Authorization','Order'])

    def __init__( self, amount=None, items=None ):
        self._nvp_request = dict()
        self._nvp_request['PAYMENTREQUEST_%d_CURRENCYCODE'] = 'EUR'
        self._items = list()
        
        if (items is None) or (len(items) == 0):
            if amount:
                self._set_fieldamount( 'PAYMENTREQUEST_0_AMT', amount )
            else:
                return
        
        for item in items:
            self._items.append( item.get_nvp_request() )

    def set_amount(self, amount):
        """(Required) Total cost of the transaction to the buyer.
        If shipping cost and tax charges are known, include them 
        in this value. If not, this value should be the current 
        sub-total of the order. If the transaction includes one 
        or more one-time purchases, this field must be equal to 
        the sum of the purchases. Set this field to 0 if the 
        transaction does not include a one-time purchase such as 
        when you set up a billing agreement for a recurring payment 
        that is not immediately charged. When the field is set 
        to 0, purchase-specific fields are ignored. You can 
        specify up to 10 payments, where n is a digit between 0 and 
        9, inclusive except for digital goods, which supports 
        single payments only."""
        self._nvp_request['PAYMENTREQUEST_%d_AMT'] = amount

    def set_currency( self, currency ):
        """(Optional) A 3-character currency code (default is USD). 
        You can specify up to 10 payments, where n is a digit between 
        0 and 9, inclusive except for digital goods, which supports 
        single payments only.""" 
        
        if currency not in static.currency_set:
            raise ValueError('Invalid currency')
        
        self._nvp_request['PAYMENTREQUEST_%d_CURRENCYCODE'] = currency

    def set_item_amount(self, item_amount ):
        """Sum of cost of all items in this order. For digital goods, 
        this field is required. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive except for 
        digital goods, which supports single payments only.
        NOTE:PAYMENTREQUEST_n_ITEMAMT is required if you specify 
        L_PAYMENTREQUEST_n_AMTm ."""
        
        self._nvp_request['PAYMENTREQUEST_%d_ITEMAMT'] = item_amount
    
    def set_shipping_amount( self, amount ):
        """Total shipping costs for this order. 
        Note: Character length and limitations: 
            Must not exceed $10,000 USD in any currency.
            No currency symbol. 
            Regardless of currency, decimal separator must be a period (.) 
            Equivalent to nine characters maximum for USD."""
        
        self._set_fieldamount('PAYMENTREQUEST_%d_SHIPPINGAMT', amount )
    
    def set_insurance_amount( self, amount, insurance_option=False ):
        """ Total shipping insurance costs for this order."""
        self._set_fieldamount( 'PAYMENT_REQUEST_%d_INSURANCEAMT', amount )
        
        if insurance_option:
            self._nvp_request['PAYMENTREQUEST_%d_INSURANCEOPTIONOFFERED'] = 'true'

    def set_shipping_discount( self, discount ):
        """Shipping discount for this order, specified as a negative number."""
        
        self._set_fieldamount( 'PAYMENTREQUEST_%d_SHIPDISCAMT', discount )

    def set_insurance_option_offered(self, value):
        """(Optional) Indicates whether insurance is available as 
        an option the buyer can choose on the PayPal Review page."""
        
        val = 'true' if value else 'false'
        self._nvp_request['PAYMENTREQUEST_%d_INSURANCEOPTIONOFFERED'] = val
    
    def set_handling_amount( self, amount ):
        """Total handling costs for this order."""
        
        validator = util.Validator()
        validator.is_new_valid_amount(amount)
        
        self._set_fieldamount( 'PAYMENTREQUEST_%d_HANDLINGAMT', amount )

    def set_tax_amount(self, amount):
        """(Optional) Sum of tax for all items in this order. You can specify up to 10 
        payments, where n is a digit between 0 and 9, inclusive except for digital goods, 
        which supports single payments only."""
        
        self._set_fieldamount('PAYMENTREQUEST_%d_TAXAMT', amount)
    
    def set_description( self, description ):
        """Description of items the customer is purchasing. 
        Character length and limitations: 127 single-byte alphanumeric characters."""
        if (description is None) or (len(description) == 0): return
        if len(description) > 127:
            raise ValueError( 'Description cannot exceed 127 characters' )
        
        self._nvp_request['PAYMENTREQUEST_%d_DESC'] = description

    def set_custom_field( self, field ):
        """A free-form field for your own use.
        Character length and limitations: 256 single-byte alphanumeric characters."""
        if (field is None) or (len(field) == 0): return
        if len(field) > 256:
            raise ValueError( 'CustomField cannot exceed 256 characters' )
        
        self._nvp_request['PAYMENTREQUEST_%d_CUSTOM'] = field


    def set_invoice_number( self, invoice_number ):
        """Your own invoice or tracking number. 
        Character length and limitations: 127 single-byte alphanumeric characters."""
        if (invoice_number is None) or (len(invoice_number) == 0): return
        if len(invoice_number) > 127:
            raise ValueError( 'invoice_number cannot exceed 127 characters' )
        
        self._nvp_request['PAYMENTREQUEST_%d_INVNUM'] = invoice_number


    def set_button_source( self, source ):
        """An identification code for use by third-party applications to identify transactions. 
        Character length and limitations: 32 single-byte alphanumeric characters."""
        if (source is None) or (len(source) == 0): return
        if len(source) > 127:
            raise ValueError( 'source cannot exceed 127 characters' )

        self._nvp_request['BUTTONSOURCE'] = source


    def set_notify_url( self, notify_url ):
        """Your URL for receiving Instant Payment Notification (IPN) about this transaction. 
        If you do not specify this value in the request, the notification URL 
        from your Merchant Profile is used, if one exists.
        
            Important: The notify URL only applies to DoExpressCheckoutPayment. 

        This value is ignored when set in SetExpressCheckout or GetExpressCheckoutDetails.

        Character length and limitations: 2,048 single-byte alphanumeric characters."""
        if (notify_url is None) or (len(notify_url) == 0): return
        if len(notify_url) > 2048:
            raise ValueError( 'notify_url cannot exceed 2048 characters' )

        self._nvp_request['PAYMENTREQUEST_%d_NOTIFYURL'] = notify_url
    

    def set_note( self, note ):
        """Note to the seller.
        Character length and limitations: 255 single-byte characters."""
        if (note is None) or (len(note) == 0): return
        if len(note) > 255:
            raise ValueError( 'notify_url cannot exceed 2048 characters' )
        
        self._nvp_request['PAYMENTREQUEST_%d_NOTETEXT'] = note
    
    def set_transaction_id( self, transaction_id ):
        """Transaction identification number of the transaction that was created."""
        
        self._nvp_request['PAYMENTREQUEST_%d_TRANSACTIONID'] = transaction_id
    
    def set_allowed_payment_method( self, method ):
        """The payment method type. 
        Specify the value: InstantPaymentOnly."""
        
        self._nvp_request['PAYMENTREQUEST_%d_ALLOWEDPAYMENTMETHOD'] = method
    
    def set_payment_action(self, value):
        """How you want to obtain payment. When implementing parallel payments, 
        this field is required and must be set to Order. When implementing digital goods, 
        this field is required and must be set to Sale. You can specify up to 10 payments, 
        where n is a digit between 0 and 9, inclusive except for digital goods, which 
        supports single payments only. If the transaction does not include a one-time 
        purchase, this field is ignored"""
        
        if value not in Payment.PAYMENT_ACTION:
            raise ValueError('Payment action value must exist in Payment.PAYMENT_ACTION')
        
        self._nvp_request['PAYMENTREQUEST_%d_PAYMENTACTION'] = value
    
    def set_payment_request_id(self, value):
        """A unique identifier of the specific payment request, 
        which is required for parallel payments."""
        if (value is None) or (len(value) == 0): return
        if len(value) > 127:
            raise ValueError( 'Payment request id cannot exceed 127 characters' )    
        
        self._nvp_request['PAYMENTREQUEST_%d_PAYMENTREQUESTID'] = value
    
    def get_nvp_request( self, payment_number=0 ):
        
        ff = util.FormatFields()
        
        nvp = copy.deepcopy( self._nvp_request )

        item_amt = 0
        item_tax = 0
        
        i = 0
        for item in self._items:
            for k, v in item.items():
                # KEYn VALUE 
                # nvp['{0}{1}'.format(k,i)] = v
                nvp[k % (payment_number,i)] = v
                # item amount
                if k == 'L_PAYMENTREQUEST_%d_AMT%d': item_amt += int( v.replace('.','') )

                # tax amount
                if k == 'L_PAYMENTREQUEST_%d_TAXAMT%d': item_tax += int( v.replace('.','') )
            
            i = i + 1

        if item_amt > 0:
            nvp[('PAYMENTREQUEST_%d_ITEMAMT' % (payment_number))] = ff.get_amount_field( (item_amt/float(100)) )

        if item_tax > 0:
            nvp['PAYMENTREQUEST_%d_TAXAMT'] = ff.get_amount_field( (item_tax/float(100)) )
        
        # set AMT if not set
        if 'PAYMENTREQUEST_%d_AMT' not in nvp:
            # calculate total - tax, shipping etc.
            total = item_amt + item_tax
            
            if 'PAYMENTREQUEST_%d_HANDLINGAMT' in nvp:
                total += int( nvp[('PAYMENTREQUEST_%d_HANDLINGAMT' % payment_number)].replace('.', '') )
            
            if 'PAYMENTREQUEST_%d_SHIPPINGAMT' in nvp:
                total += int( nvp[('PAYMENTREQUEST_%d_SHIPPINGAMT' % payment_number)].replace('.', '') )
            
            # convert back to two decimals
            total = total / float(100)
            nvp[('PAYMENTREQUEST_%d_AMT' % payment_number)] = ff.get_amount_field( total )
        
        # handling or shipping amount is set but item amount is not set
        if ((('PAYMENTREQUEST_%d_HANDLINGAMT' % payment_number) in nvp) or (('PAYMENTREQUEST_%d_SHIPPINGAMT' % payment_number) in nvp)) and (('PAYMENTREQUEST_%d_ITEMAMT' % payment_number) not in nvp):
            # set the amount for itemamt - because itemamt is required when handling amount is set
            nvp[('PAYMENTREQUEST_%d_ITEMAMT' % payment_number)] = nvp[('PAYMENTREQUEST_%d_AMT' % payment_number)]
        
        return nvp


    def _set_fieldamount( self, field, amount ):
        v = util.Validator()
        if not v.is_new_valid_amount( amount ):
            sb = StringIO.StringIO()
            sb.write( 'Amount {0} is not valid. '.format(amount) )
            sb.write( 'Amount has to have exactly two decimal ' )
            sb.write( 'places seaprated by \".\" ' )
            sb.write( '- example: \"50.00\"' )
            raise ValueError( sb.getvalue() )
        del ( v )

        ff = util.FormatFields()
        amount = ff.get_new_amount_field( amount )
        self._nvp_request[field] = amount

class PaymentMulti( RequestFields ):

    """Holds a list of Payment"""
    
    payment_action = set(['Sale','Authorization','Order'])

    def __init__( self ):
        self._nvp_request = dict()
        self._nvp_request['PAYMENTREQUEST_%d_CURRENCYCODE'] = 'EUR'
        self._items = list()
    """    
        if (items is None) or (len(items) == 0):
            if amount:
                self._set_fieldamount( 'PAYMENTREQUEST_0_AMT', amount )
            else:
                return
        
        if len(items) > 10:
            raise ValueError('There can not be more than 10 payments')
        
        for item in items:
            self._items.append(item)
    """
    def get_nvp_request( self ):
        
        i = 0
        nvp = {}
        for item in self._items:
            nvp.update(item.get_nvp_request(i))
            i+=1
        
        return nvp
        
    

class UserSelectedOptions( RequestFields ):

    def __init__( self ):
        self._nvp_request = dict()


    def set_shipping_calculation( self, calculation ):
        """Describes how the options that were presented to 
        the user were determined."""
        if calculation not in ['CALLBACK', 'FLATRATE']:
            raise ValueError( 'calculation must be CALLBACK or FLATRATE' )

        self._nvp_request['SHIPPINGCALCULATIONMODE'] = calculation


    def set_insurance( self, insurance ):
        """The Yes/No option that you chose for insurance."""
        flag = 'Yes' if insurance else 'No'
        self._nvp_request['INSURANCEOPTIONSELECTED'] = flag


    def set_default_shipping_option( self, option ):
        """Is true if the buyer chose the default shipping option."""
        flag = 'true' if option else 'false'
        self._nvp_request['SHIPPINGOPTIONISDEFAULT'] = flag
        if option:
            self._nvp_request['SHIPPINGOPTIONNAME'] = flag


    def set_shipping_amount( self, amount ):
        """The shipping amount that was chosen by the buyer 
        Limitations:

            - Must not exceed $10,000 USD in any currency.
            - No currency symbol. 
            - Must have two decimal places, decimal separator must be a period (.)."""
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            sb = StringIO.StringIO()
            sb.write( 'Amount {0} is not valid. '.format(amount) )
            sb.write( 'Amount has to have exactly two decimal ' )
            sb.write( 'places seaprated by \".\" ' )
            sb.write( '- example: \"50.00\"' )
            raise ValueError( sb.getvalue() )
        del ( v )

        ff = util.FormatFields()
        amount = ff.get_amount_field( amount )
        self._nvp_request['SHIPPINGOPTIONAMOUNT'] = amount


    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)

class ScheduleDetails( RequestFields ):
    
    def __init__(self, description):
        
        if (description is None) or (len(description) >= 127):
            raise ValueError( 'Invalid description argument' )
        
        self._nvp_request = dict()
        self._nvp_request['DESC'] = description
        
    def set_max_failed_payments(self, number):
        self._nvp_request['MAXFAILEDPAYMENTS'] = str(number)
    
    def set_auto_bill_amount(self, autobill):
        value = 'AddToNextBilling' if autobill else 'NoAutoBill'
        self._nvp_request['AUTOBILLAMT'] = value
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
class BillingPeriodDetails( RequestFields ):
    
    billing_period = (['Day','Week','SemiMonth','Month','Year'])
    
    def __init__(self, period, frequency, amount, currency):
        
        billing_frequency = str(frequency)
        
        if frequency < 0:
            raise ValueError('Billing frequency cannot be 0')
        
        if period == 'Year' and frequency > 365:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Month' and frequency > 12:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Week' and frequency > 52:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Day' and frequency > 1:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'SemiMonth' and frequency is not 1:
            raise ValueError('When billing period is set to Semi month, then billing frequency has to be 1: (%s, %s)' % (billing_frequency, str(period)))
        
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            raise ValueError('Amount has to have exactly two decimal places separated by \'.\' - example: \'50.00\'')
        
        if currency not in static.currency_set:
            raise ValueError('Invalid currency')
        
        self._nvp_request = dict()
        
        self._nvp_request['BILLINGPERIOD'] = period
        self._nvp_request['BILLINGFREQUENCY'] = frequency
        self._nvp_request['AMT'] = amount
        self._nvp_request['CURRENCYCODE'] = currency
    
    def set_total_billing_cycles(self, billing_cycles):
        self._nvp_request['TOTALBILLINGCYCLES'] = billing_cycles
    
    def set_trial_billing(self, period, frequency, amount):
        billing_frequency = str(frequency)
        
        if frequency < 0:
            raise ValueError('Billing frequency cannot be 0')
        
        if period == 'Year' and frequency > 365:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Month' and frequency > 12:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Week' and frequency > 52:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'Day' and frequency > 1:
            raise ValueError('The combination of billing frequency (%s) and billing period (%s) must be less than or equal to one year.' % (billing_frequency,period))
        elif period == 'SemiMonth' and frequency is not 1:
            raise ValueError('When billing period is set to Semi month, then billing frequency has to be 1: (%s, %s)' % (billing_frequency, str(period)))
        
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            raise ValueError('Amount has to have exactly two decimal places separated by \'.\' - example: \'50.00\'')
        
        self._nvp_request = dict()
        
        self._nvp_request['TRIALBILLINGPERIOD'] = period
        self._nvp_request['TRIALBILLINGFREQUENCY'] = billing_frequency
        self._nvp_request['TRIALAMT'] = amount
    
    def set_trial_billing_cycles(self, billing_cycles):
        self._nvp_request['TRIALTOTALBILLINGCYCLES'] = str(billing_cycles)
        
    def set_shipping_amount(self, amount):
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            raise ValueError('Amount has to have exactly two decimal places separated by \'.\' - example: \'50.00\'')
        
        self._nvp_request['SHIPPINGAMT'] = amount
    
    def set_tax_amount(self, amount):
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            raise ValueError('Amount has to have exactly two decimal places separated by \'.\' - example: \'50.00\'')
        
        self._nvp_request['TAXAMT'] = amount
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)

class RecurringPaymentsProfileDetails( RequestFields ):
    def __init__(self,profile_start_date):
        f = util.FormatFields()
        date = f.get_datetime_field(profile_start_date)
        self._nvp_request = {}
        self._nvp_request['PROFILESTARTDATE'] = date
    
    def set_subscriber_name(self, name):
        if len(name) > 32:
            raise ValueError('Name can be maximum 32 characters')
        
        self._nvp_request['SUBSCRIBERNAME'] = name
    
    def set_profile_reference(self, reference_number):
        if len(reference_number) > 127:
            raise ValueError('Reference number can be maximum 32 characters')
        
        self._nvp_request['PROFILEREFERENCE'] = reference_number
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
class ActivationDetails( RequestFields ):
    def __init__(self):
        self._nvp_request = {}
    
    def set_initial_amount(self, amount):
        v = util.Validator()
        if not v.is_valid_amount( amount ):
            raise ValueError('Amount has to have exactly two decimal places separated by \'.\' - example: \'50.00\'')
        self._nvp_request['INITAMT'] = amount
        
    def set_failed_initial_amount_action(self, continue_on_failure):
        value = 'ContinueOnFailure' if continue_on_failure else 'CancelOnFailure'
        self._nvp_request['FAILEDINITAMTACTION'] = value
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
class PayerInformation( RequestFields ):
    
    PAYER_STATUS = set(['verified','unverified'])
    
    def __init__(self):
        self._nvp_request = {}
    
    def set_email(self, email):
        v = util.Validator()
        if not v.is_valid_email( email ):
            raise ValueError('Email is not valid')
        if email is None or len(email) > 127:
            raise ValueError('Email can be maximum 127 characters long')
        self._nvp_request['EMAIL'] = email
    
    def set_payer_id(self, payer_id):
        if payer_id is None or len(payer_id) > 13:
            raise ValueError('PayerId can be maximum 13 alphanumeric characters long')
        self._nvp_request['PAYERID'] = payer_id
        
    def set_payer_status(self, status):
        if status not in PayerInformation.PAYER_STATUS:
            raise ValueError('PayerStatus value invalid')
        self._nvp_request['PAYERSTATUS'] = status
    
    def set_country(self, country):
        if country not in static.country_dict:
            raise ValueError('Country code not found')
        self._nvp_request['COUNTRYCODE'] = static.country_dict[country]
    
    def set_business_name(self, name):
        if name is not None and len(name)>127:
            raise ValueError('Name can be maximum 127 characters long')
        self._nvp_request['BUSINESS'] = name
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
class PayerName( RequestFields ):
    def __init__(self):
        self._nvp_request = {}
        
    def set_salutation(self, salutation):
        if len(salutation) > 20:
            raise ValueError('Salutation can be maximum 20 characters long')
        self._nvp_request['SALUTATION'] = salutation
        
    def set_first_name(self, first_name):
        if len(first_name) > 25:
            raise ValueError('FirstName can be maximum 25 characters long')
        self._nvp_request['FIRSTNAME'] = first_name
    
    def set_middle_name(self, middle_name):
        if len(middle_name) > 25:
            raise ValueError('MiddleName can be maximum 25 characters long')
        self._nvp_request['MIDDLENAME'] = middle_name
    
    def set_last_name(self, last_name):
        if len(last_name) > 25:
            raise ValueError('LastName can be maximum 25 characters long')
        self._nvp_request['LASTNAME'] = last_name
    
    def set_suffix(self, suffix):
        if len(suffix) > 12:
            raise ValueError('Suffix can be maximum 12 characters long')
        self._nvp_request['SUFFIX'] = suffix
        
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
