# -*- coding: cp1252 -*-
# $Id: GPSReader.py 33 2010-05-06 17:21:14Z cfluegel $

# TODO 
# - Einige Variablen zu "private" Variablen umwandeln
# - Dokumentation vervollstaendigen 

#### Importbereich
import serial, time, sys
import threading

import NMEAtelegrams
from GPSError import *

#### GPS Main class                 
class GPSReader(threading.Thread, object):
  """ GPSReader - Handles the communication with a GPS reader of a phy or virt interface

  This class connects to a virt or phy serial interface and reads different NMEA sentence.
  Currently the following NMEA sentences will be converted to different classes: GGA, RMC, VTG
  but more are planed.

  At the moment there are no plans to communicate two-way with a GPS receiver. """
  def __init__(self, comport=None):
    self._SerialObj = None
    self._rawdata = None
    self._stop = threading.Event()
    self.GGA = None
    self.VTG = None
    self.RMC = None


    # No serial port? Error!
    if (comport == None):
      raise GPSCommError()
    self.connectToComport(comport)

    # let the __init__ of threading do some work :) 
    threading.Thread.__init__(self)

    # Start the thread automatically 
    self.daemon = True
    self.start()

  def __del__(self):
    # Master, shall I remove the connection the serial interface? Yes! 
    self.disconnect()

  def connectToComport(self, comport):
    """ Opens the comport with a fixed baudrate of 4800 and a timeout of 10seconds 
    or throw a execption if no connection can be established. """
    try:
      self._SerialObj = serial.Serial(port=comport, baudrate=4800, timeout=10)
    except serial.SerialException:
      raise GPSCommError("Connection with Comport failed!")

  def disconnect(self):
    """ Closes the connection to the serial interface """
    if self._SerialObj <> None:
      self._SerialObj.close()

  def isConnected(self):
    """ Wrapper for the actual isOpen() of pyserial """
    if self._SerialObj <> None:
      return self._SerialObj.isOpen()

  def stop_thread(self):
    """ Stop the thread flag which is herewith set """
    self._stop.set()

  def join(self, timeout=None):
    self._stop.set()
    threading.Thread.join(self,timeout)

  def getRawdata(self):
    """ Lets you watch the rawdata in case something is bothering you :D"""
    return self._rawdata

  def run(self):
    """ threading.Thread.run() overloaded. Here the actual stuff is going on. 

    Converts the different NMEA sentences into seperated classes which allow one 
    better access to the different sentences. The classes have different methodes
    to access the fields."""
    self.GGA = NMEAtelegrams.NMEA_GGA()
    self.VTG = NMEAtelegrams.NMEA_VTG()
    self.RMC = NMEAtelegrams.NMEA_RMC()

    while True:
      if (self._stop.isSet()):
        self.disconnect()
        break

      t_sentence = self._SerialObj.readline().strip("\r\n")
      if len(t_sentence) > 0:
        self._rawdata = t_sentence  # RAW Sentence speichern fuer Debug Zwecke

        if ( ("GGA" in t_sentence) and (NMEAtelegrams.VerifyNMEAChkSum(t_sentence) == True) ):
          self.GGA.parseSentence(t_sentence)
        elif ( ("VTG" in t_sentence) and (NMEAtelegrams.VerifyNMEAChkSum(t_sentence) == True) ):
          self.VTG.parseSentence(t_sentence)
        elif ( ("RMC" in t_sentence) and (NMEAtelegrams.VerifyNMEAChkSum(t_sentence) == True) ):
          self.RMC.parseSentence(t_sentence)

###### TEST ####### 
# section in where I test most stuff of the current module until I figured out the nose or other 
# unittests are working. 
if __name__ == '__main__':
  try:
    test = GPSReader("COM4")
    counter = 0
    while (True and test.isAlive()):
      try:
        print "Still alive! -Pos- ", test.GGA
        print "Still alive! -LOC- ", test.GGA.getPosition()
      except NMEANoValidFix:
        print "No Valid Fix yet!"

      try:
        print "Still alive! -VTG- ", test.VTG
        print "Still alive! -COG- ", test.VTG.getCourse()
        print "Still alive! -SOG- ", test.VTG.getSpeed()
      except NMEANoValidFix:
        print "No Valid Fix yet!" 
      time.sleep(1)

      if (counter >= 10):
        test.stop_thread()
      counter = counter + 1
  except GPSCommError as e :
     print "some error occured during the start "
     print "it says: ",  e
     sys.exit(3)
  except KeyboardInterrupt:
    test.disconnect()

  sys.exit(0)
