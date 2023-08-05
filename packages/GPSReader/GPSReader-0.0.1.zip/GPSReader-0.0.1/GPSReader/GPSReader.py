# -*- coding: cp1252 -*-
# $Id: GPSReader.py 26 2010-04-03 17:52:24Z cfluegel $

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
  """ GPSReader - Kommunikation mit einem GPS Geraet (NMEA)
  Ermoeglicht die Verbindung zu einem GPS Geraet ueber die serille Schnittstelle
  eines Computers. Es werden derzeit nur die Telegramme von einem GPS Geraet 
  verarbeitet.

  Eine Bidirektionale Kommunikation ist derzeit nicht geplant."""
  def __init__(self, comport=None):
    self._SerialObj = None
    self._rawdata = None
    self._stop = threading.Event()
    self.GGA = None
    self.VTG = None
    self.RMC = None


    # Falls kein COMPort angegeben worden ist, Fehler produzieren
    # sonst mit COM Port Verbinden und probieren zu setzen
    if (comport == None):
      raise GPSCommError()
    self.connectToComport(comport)

    # __init__ der geerbten Klasse aufrufen. 
    threading.Thread.__init__(self)

    # Automatisches wird hier aktiviert 
    self.daemon = True
    self.start()

  def __del__(self):
    # Verbindung mit dem GPS oesen
    self.disconnect()

  def connectToComport(self, comport):
    """ Oeffnet ein ComPort, derzeit nur auf Windows, zum lesen mit der festen Baudrate 4800 
    und einem Timeout von 10 Sekunden bis das Programm aufhoert nach Daten zu gucken."""
    try:
      self._SerialObj = serial.Serial(port=comport, baudrate=4800, timeout=10)
    except serial.SerialException:
      raise GPSCommError("COM Port konnte nicht geoeffnet werden!")

  def disconnect(self):
    """ Schliesst die geoeffnete Verbindung wieder. """
    if self._SerialObj <> None:
      self._SerialObj.close()

  def connectedToComport(self):
    """ Wrapper Methode um auf den Verbindungsstatus zuzugreifen. """
    if self._SerialObj <> None:
      return self._SerialObj.isOpen()

  def stop_thread(self):
    """ setzt ein im Thread bekanntes flag, welches den Thread anweist sicht selbst zu beenden """
    self._stop.set()

  def join(self, timeout=None):
    self._stop.set()
    threading.Thread.join(self,timeout)

  def run(self):
    """ threading.Thread.run() ueberladen, damit diese Komponente die Daten des GPS im Hintergrund
    auslesen und verarbeiten kann. Somit kann das Hauptprogramm weitere Dinge mit den Daten machen."""
    self.GGA = NMEA.NMEA_GGA()
    self.VTG = NMEA.NMEA_VTG()
    self.RMC = NMEA.NMEA_RMC()

    while True:
      if (self._stop.isSet()):
        self.disconnect()
        break

      t_sentence = self._SerialObj.readline().strip("\r\n")
      if len(t_sentence) > 0:
        self._rawdata = t_sentence  # RAW Sentence speichern fuer Debug Zwecke

        # Standardmaessig wird GGA ausgewertet... sollte man nicht RMC ausgewählt haben. 
        if ( ("GGA" in t_sentence) and (NMEA.VerifyNMEAChkSum(t_sentence) == True) ):
          self.GGA.parseSentence(t_sentence)
        elif ( ("VTG" in t_sentence) and (NMEA.VerifyNMEAChkSum(t_sentence) == True) ):
          self.VTG.parseSentence(t_sentence)
        elif ( ("RMC" in t_sentence) and (NMEA.VerifyNMEAChkSum(t_sentence) == True) ):
          self.RMC.parseSentence(t_sentence)

###### TEST #######  
if __name__ == '__main__':
  try:
    test = GPSReader("COM4")
    print test.connectedToComport()
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

