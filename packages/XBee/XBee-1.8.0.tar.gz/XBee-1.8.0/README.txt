=========
XBee
=========

XBee provides an implementation of the XBee serial communication API. It
allows one to easily access advanced features of one or more XBee
devices from an application written in Python. An example use case might
look like this::

    #! /usr/bin/python
    
    # Import and init an XBee device
    from xbee import XBee
    import serial

    ser = serial.Serial('/dev/ttyUSB0', 9600)
    xbee = XBee(ser)
    
    # Set remote DIO pin 2 to low (mode 4)
    xbee.remote_at(
      dest_addr='\x56\x78',
      command='D2',
      parameter='\x04')
      
    xbee.remote_at(
      dest_addr='\x56\x78',
      command='WR')
      
      
Usage
============

Series 1, Series 2
------------------

To use this library with an XBee device, import the class
XBee and call its constructor with a serial port object.

In order to send commands via the API, call a method with the same
name as the command which you would like to send with words separated
by _'s. For example, to send a Remote AT command, one would call 
remote_at().

The arguments to be given to each method depend upon the command to be 
sent. For more information concerning the names of the arguments which
are expected and the proper data types for each argument, consult the
API manual for your XBee device, or consult the source code.

Caveats
---------

Escaped API operation has not been implemented at this time.

Dependencies
============

PySerial

Additional Dependencies (for running tests):
--------------------------------------------

Nose

XBee Firmware
-------------

Please ensure that your XBee device is programmed with the latest firmware
provided by Digi. Using old firmware revisions is not supported and
may result in unspecified behavior.

Contributors
==================

Paul Malmsten <pmalmsten@gmail.com>

Special Thanks
==================

Amit Synderman,
Marco Sangalli
