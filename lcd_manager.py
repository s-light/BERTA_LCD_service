#!/usr/bin/python
# coding=utf-8

"""
LCD Manager script.

    script to show different system information on I2C LCD.
    configuration in config.json

    http://www.acmesystems.it/arietta_daisy24

    used libraries:
        ablib

    history:
        see git commits

    todo:
        ~ research and implement things
        ~ all fine :-)
"""


import sys
import os
import array
import time

from configdict import ConfigDict

# http://wiki.python-forum.de/Import
try:
    import ablib
    ablib_available = True
except ImportError:
    import warnings
    warnings.warn("exception while importing Module 'ablib' !")
    print(""" Check to run your script with SUDO.""")
    ablib_available = False
#

version = """10.05.2016 21:16 stefan"""


##########################################
# globals


##########################################
# functions


##########################################
# classes

class LCDManager():
    """Main Class."""

    default_config = {
        'lcd_address': 0x27,
        'show': {
            'line1': ':-)',
        },
    }

    def __init__(self, filename):
        """init."""
        # read config file:
        self.my_config = ConfigDict(self.default_config, filename)
        # print("my_config.config: {}".format(self.my_config.config))
        self.config = self.my_config.config
        # print("config: {}".format(self.config))
        self._init_lcd()

    def __del__(self):
        """Clean up."""
        pass

    ##########################################
    #
    def config_print(self):
        """Print configuration."""
        print("config: \n{}".format(self.my_config.get_formated()))
        # print(42*'*')

    ##########################################
    #

    def _init_lcd(self):
        print("init lcd:")
        if ablib_available:
            print("ablib available.")
            try:
                if ablib.existI2Cdevice(0, self.config['lcd_address']):
                    i2c_address = self.config['lcd_address']
                else:
                    i2c_address = 0x3F
                print("  i2c_address:{}".format(i2c_address))
                self.lcd = ablib.Daisy24(0, i2c_address)
                print("  lcd:{}".format(self.lcd))
            except Exception as e:
                raise
                print(""" Check to run your script with SUDO.""")
                ablib_available = False
        else:
            print("ablib missing!!!!!!!")

    def _write_lcd(self):
        if ablib_available:
            self.lcd.setcurpos(0, 0)
            self.lcd.putstring('Hello World :-)')
            self.lcd.setcurpos(0, 1)
            self.lcd.putstring('sunshine :-)')

    def system_run(self):
        """Run Main Loop."""
        print("Start Main Loop: TODO!!!")
        self._write_lcd()


##########################################
if __name__ == '__main__':

    print(42*'*')
    print('Python Version: ' + sys.version)
    print(42*'*')
    print(__doc__)
    print(42*'*')

    flag_save_config = False

    # parse arguments
    filename = "config.json"
    # only use args after script name
    arg = sys.argv[1:]
    if not arg:
        print("using standard values.")
        print(" Allowed parameters:")
        print("   filename for config file       (default='config.json')")
        print("")
    else:
        filename = arg[0]
        if len(arg) > 1:
            if '-s' in arg[1]:
                flag_save_config = True
    # print parsed argument values
    print('''values:
        filename :{}
    '''.format(filename))

    my_lcdmanager = LCDManager(filename)

    my_lcdmanager.system_run()

    if flag_save_config:
        my_lcdmanager.my_config.write_to_file()

    # ###########################################
