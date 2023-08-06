#!/usr/bin/env python
#
#   Copyright 2011 Jonas Berg
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

"""

.. moduleauthor:: Jonas Berg <pyhys@users.sourceforge.net>

Driver for the Eurotherm3500 process controller, for communication via the Modbus RTU protocol.

This Python file was changed (committed) at 
$Date: 2011-08-19 11:43:37 +0200 (Fri, 19 Aug 2011) $, 
which was $Revision: 55 $.

"""

__author__  = "Jonas Berg"
__email__   = "pyhys@users.sourceforge.net"
__license__ = "Apache License, Version 2.0"

__version__   = "0.20"
__status__    = "Alpha"
__revision__  = "$Rev: 55 $"
__date__      = "$Date: 2011-08-19 11:43:37 +0200 (Fri, 19 Aug 2011) $"

import minimalmodbus

class Eurotherm3500( minimalmodbus.Instrument ):
    """Instrument class for Eurotherm 3500 process controller. 
    
    Communicates via Modbus RTU protocol (via RS232 or RS485), using the *MinimalModbus* Python module.    

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """
    
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
    
    ## Process value
    
    def get_pv_loop1(self):
        """Return the process value (PV) for loop1."""
        return self.read_register(289, 1)
    
    def get_pv_loop2(self):
        """Return the process value (PV) for loop2."""
        return self.read_register(1313, 1)
    
    ## Auto/manual mode
    
    def is_manual_loop1(self):
        """Return the True if loop1 is in man mode."""
        return self.read_register(273, 1) > 0
    
    ## Setpoint
    
    def get_sptarget_loop1(self):
        """Return the setpoint (SP) target for loop1."""
        return self.read_register(2, 1)
    
    def get_sp_loop1(self):
        """Return the (working) setpoint (SP) for loop1."""
        return self.read_register(5, 1)
    
    def set_sp_loop1(self, value):
        """Set the SP1 for loop1.
        
        Note that this is not necessarily the working setpoint.

        Args:
            value (float): Setpoint (most often in degrees)
        """
        self.write_register(24, value, 1)
    
    def get_sp_loop2(self):
        """Return the (working) setpoint (SP) for loop2."""
        return self.read_register(1029, 1)
    
    ## Setpoint rate
    
    def get_sprate_loop1(self):
        """Return the setpoint (SP) change rate for loop1."""
        return self.read_register(35, 1)   
    
    def set_sprate_loop1(self, value):
        """Set the setpoint (SP) change rate for loop1.
        
        Args:
            value (float): Setpoint change rate (most often in degrees/minute)

        """
        self.write_register(35, value, 1)  
    
    def is_sprate_disabled_loop1(self):
        """Return True if Loop1 setpoint (SP) rate is disabled."""
        return self.read_register(78, 1) > 0

    def disable_sprate_loop1(self):
        """Disable the setpoint (SP) change rate for loop1. """
        VALUE = 1
        self.write_register(78, VALUE, 0) 
        
    def enable_sprate_loop1(self):
        """Set disable=false for the setpoint (SP) change rate for loop1.
        
        Note that also the SP rate value must be properly set for the SP rate to work.
        """
        VALUE = 0
        self.write_register(78, VALUE, 0) 
    
    ## Output signal
    
    def get_op_loop1(self):
        """Return the output value (OP) for loop1 (in %)."""
        return self.read_register(85, 1)
   
    def is_inhibited_loop1(self):
        """Return True if Loop1 is inhibited."""
        return self.read_register(268, 1) > 0

    def get_op_loop2(self):
        """Return the output value (OP) for loop2 (in %)."""
        return self.read_register(1109, 1)
    
    ## Alarms

    def get_threshold_alarm1(self):
        """Return the threshold value for Alarm1."""
        return self.read_register(10241, 1)
    
    def is_set_alarmsummary(self):
        """Return True if some alarm is triggered."""
        return self.read_register(10213, 1) > 0
    
########################
## Testing the module ##
########################

if __name__ == '__main__':
    import sys
    def print_out( inputstring ):
        """Print the inputstring. To make it compatible with Python2 and Python3."""
        sys.stdout.write(inputstring + '\n') 

    print_out( 'TESTING EUROTHERM 3500 MODBUS MODULE')

    a = Eurotherm3500('/dev/cvdHeatercontroller', 1)
    
    print_out( 'SP1:                    {0}'.format(  a.get_sp_loop1()             ))
    print_out( 'SP1 target:             {0}'.format(  a.get_sptarget_loop1()       ))
    print_out( 'SP2:                    {0}'.format(  a.get_sp_loop2()             ))
    print_out( 'SP-rate Loop1 disabled: {0}'.format(  a.is_sprate_disabled_loop1() ))
    print_out( 'SP1 rate:               {0}'.format(  a.get_sprate_loop1()         ))
    print_out( 'OP1:                    {0}%'.format( a.get_op_loop1()             ))
    print_out( 'OP2:                    {0}%'.format( a.get_op_loop2()             ))
    print_out( 'Alarm1 threshold:       {0}'.format(  a.get_threshold_alarm1()     ))
    print_out( 'Alarm summary:          {0}'.format(  a.is_set_alarmsummary()      ))
    print_out( 'Manual mode Loop1:      {0}'.format(  a.is_manual_loop1()          ))
    print_out( 'Inhibit Loop1:          {0}'.format(  a.is_inhibited_loop1()       ))
    print_out( 'PV1:                    {0}'.format(  a.get_pv_loop1()             ))
    print_out( 'PV2:                    {0}'.format(  a.get_pv_loop2()             ))

    #a.set_sp_loop1(5)
    #a.set_sprate_loop1(20)
    #a.enable_sprate_loop1() 
    #a.disable_sprate_loop1() 
    
    print_out( 'DONE!' )

pass    
