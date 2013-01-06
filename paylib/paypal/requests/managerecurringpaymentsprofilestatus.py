# Copyright (C) 2012 Client Side Web <rutherford@clientsideweb.net>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy

from paylib.paypal import core

class ManageRecurringPaymentsProfileStatus(core.Request):
    
    """The ManageRecurringPaymentsProfileStatus API operation cancels, 
    suspends, or reactivates a recurring payments profile."""
    
    action = set(['Cancel','Suspend','Reactivate'])
    
    def __init__(self, profile_id, action, note=None):
        
        if (profile_id is None) or (len(profile_id) not in [14,19]):
            raise ValueError( 'Invalid profile id argument' )
        if action not in ManageRecurringPaymentsProfileStatus.action:
            raise ValueError('Action must be a member of ManageRecurringPaymentsProfileStatus.action set')
        
        self._nvp_response = None
        self._nvp_request = dict()
        self._nvp_request['METHOD'] = 'ManageRecurringPaymentsProfileStatus'
        self._nvp_request['PROFILEID'] = profile_id
        self._nvp_request['ACTION'] = action
        
        if note is not None:
            self._nvp_request['NOTE'] = note
    
    def get_nvp_request( self ):
        return copy.deepcopy( self._nvp_request )
    
    def set_nvp_response( self, nvp_response ):
        if not isinstance( nvp_response, dict ):
            raise ValueError( 'nvp_response must be a <dict>.' )
        self._nvp_response = copy.deepcopy( nvp_response )
    
    def get_nvp_response( self ):
        return copy.deepcopy( self._nvp_response )
