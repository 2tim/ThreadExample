#!/usr/bin/env python
'''
Created on Jul 24, 2013

@author: Kevin Evans

@summary: The following code sample takes a 1000 element array and updates each
item in the array by setting them to 0 and then concurrent threads are
created to each add 1 to each item in the array. The resulting array
should contain 1000 items each set to 2. Access control to the array
elements is controlled by the lock object. When the array updating is
completed the resulting array is validated to contain the correct values
for each item.

@note: An array was explicitly chosen over a python list to meet the requirement
and to have better performance which is important with a multi-threaded environment.

@requires: Python 2.7.5
@note: Tested on MacBook Pro Intel Core 2 Duo
'''

import sys
import logging
import array
import threading
from itertools import repeat

class ThreadSafeArray(object):
    
    def __init__(self):
        #Logging needs to be setup to work in IDE console and command line
        self.logger = logging.getLogger("ThreadSafeArray")
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        
    def arrayUpdater(self, array_for_updating, myLock):
        for idx in range(len(array_for_updating)):
            myLock.acquire()
            try:
                array_for_updating[idx] += 1
            except:
                self.logger.error("Could not acquire a lock")
            finally:
                myLock.release()
                
                
    def validateArray(self, array_for_checking):
        badegg=0
        for item in array_for_checking:
            if item != 2:
                self.logger.error("Didn't update the array properly")
                badegg+=1
        if badegg > 0:
            self.logger.error("There were " + str(badegg) + " items that were not updated properly")
        else:
            self.logger.info("All numbers in the array were updated properly")
            
    
    def arrayThreader(self, ary):
        #Acquire a lock object to control exclusive access to the array during an update
        myLock = threading.Lock()
        #Acquire the thread objects
        t = threading.Thread(target=self.arrayUpdater, args = (ary, myLock))
        w = threading.Thread(target=self.arrayUpdater, args = (ary, myLock))
        #Start each thread so that they run concurrently through the array to update it
        t.start()
        w.start()
        #Wait for the threads to complete before moving forward
        t.join()
        w.join()
        
    def run(self):
        #Create the 1000 element array and use the repeat function to fill the array with zeros
        #Array type H is an unsigned short which has the best performance and space used.
        numberarray = array.array('H', repeat(0, 1000))
        self.arrayThreader(numberarray)
        self.validateArray(numberarray)        

def main():
    arraybuilder = ThreadSafeArray()
    arraybuilder.run()
    
if __name__ == '__main__':
    main()