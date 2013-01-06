#!/usr/bin/python

import doctest
import sys
import os

def test_harness():
    dir = os.path.dirname(__file__)
    new_dir = os.path.join(dir,'..')
    sys.path.append(new_dir)
    
    import paylib.paypal.requests.setexpresscheckout
    doctest.testmod(paylib.paypal.requests.setexpresscheckout)

if __name__ == "__main__":
    test_harness()
