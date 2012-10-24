#!/usr/bin/python

import doctest
import sys
import os

def test_harness():
	dir = os.path.dirname(__file__)
	new_dir = os.path.join(dir,'..')
	sys.path.append(new_dir)
	
	import csw.ecommerce.paypal.requests.setexpresscheckout
	doctest.testmod(csw.ecommerce.paypal.requests.setexpresscheckout)

if __name__ == "__main__":
	test_harness()