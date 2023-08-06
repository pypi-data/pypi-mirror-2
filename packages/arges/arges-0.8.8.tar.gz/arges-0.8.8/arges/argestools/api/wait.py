# -*- coding: latin-1 -*-

""" wait - a pause in seconds

@author Adri�n Deccico
"""

import logging
import time


#exposed command to the test api
def runCommand(seconds, dummy, dummy2):
    logging.debug("waiting: " + str(seconds))
    time.sleep(float(seconds))
    return True
    

