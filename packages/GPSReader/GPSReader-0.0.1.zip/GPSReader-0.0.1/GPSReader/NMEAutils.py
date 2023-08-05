# -*- coding: cp1252 -*-
# $Id: NMEAutils.py 26 2010-04-03 17:52:24Z cfluegel $

# Benoetigt fuer calculateDistance & calculateBearing
import math


############################################################################
# Helper Funktionen fuer die unterschiedlichsten Aufgaben 
############################################################################
def CreateNMEAChkSum(sentence=None):
  """ Erstellt eine XOR Checksumme einer NMEA Nachricht und gibt den Hex-Wert 
  als String zurueck."""
  if sentence == None:
    return None
  elif (sentence[0] == "$") and (sentence[-3] == "*"):
    t = sentence[1:-3]
    sentence = t
  elif (sentence[0] == "$") and (sentence[-1] == "*"):
    t = sentence[1:-1]
    sentence = t
  elif (sentence[0] == "$"):
    t = sentence[1]
    sentence = t

  i = int(0)
  XOR = int(0)
  ilen = long()
  ilen = len(sentence)

  for i in range(0,len(sentence)):
    XOR = XOR ^ ord(sentence[i])

  if (XOR <= 15):
    return "0"+str(hex(XOR))[-1:]
  else:
    return str(hex(XOR))[-2:]
# CreateNMEAChkSum

def VerifyNMEAChkSum(sentence=None):
  """ Prueft die Checksumme einer NMEA Nachricht auf Gueltigkeit. """
  if sentence == None:
    return None

  Checksum = str(sentence[-2:])
  GenChecksum = CreateNMEAChkSum(sentence)

  if (Checksum.upper() == GenChecksum.upper()):
    return True
  return False
# VerifyNMEAChkSum


def parseLatitude(lat, ns):
  """ Wandelt die Position aus dem Wertepaar Coord und N/S in
  eine positive oder negative Latitude Position um."""
  # latitude umwandeln
  # fuer testzwecke derzeit ein haessliches 
  # try ... except 
  try:
    lat_in = float(lat)
  except:
    print "Uebergeben: %s %s" % (lat,ns)

  # copied from another class
  if ns == 'S':
    lat_in = -lat_in

  latitude_degrees = int(lat_in/100)
  latitude_minutes = lat_in - latitude_degrees*100

  latitude = latitude_degrees + (latitude_minutes/60)
  return latitude
# parseLatitude

def parseLongitude(lon, ew):
  """ Wandelt die Longitude aus dem Wertepaar Coord und E/W in
  eine positive oder negative Longitude Position um."""
  # longitude umwandeln
  # fuer testzwecke derzeit ein haessliches 
  # try ... except 
  try:
    lon_in = float(lon)
  except:
    print "Uebergeben: %s %s" % (lon,ew)

  # copied from another class
  if ew == 'W':
    lon_in = -lon_in

  longitude_degrees = int(lon_in/100)
  longitude_minutes = lon_in - longitude_degrees*100

  longitude = longitude_degrees + (longitude_minutes/60)
  return longitude
# parse Longitude


def estimateDirection(CurrentCourse,DestCourse):
  """ Diese Funktion soll die Richtung bestimmen in die man Lenken/Steuern
  muss, um schnell zu dem Zielkurs zu kommen.

  Die Funktion liefert positive Zahlen bei Kursunterschied von 179 im
  Uhrzeigersinn; negative Zahlen bei Kursunterschied von > 180 Grad.
  Ferner wird die differenz zu CurrentCourse und Ziel Kurs zurückgegeben."""

  CourseCorrection = DestCourse - CurrentCourse
  if (CourseCorrection == 180):
    return 180
  if (CourseCorrection > 180):
    return -(360 - CourseCorrection)
  else:
    return CourseCorrection
# estimateDirection


class GPSPosition(object):
  def __init__(self, ilat, ilon):
    self.latitude =None
    self.longitude = None

    if type(ilat) == type( tuple() ):
      self.latitude = parseLatitude( ilat[0], ilat[1] )
    if type(ilon) == type( tuple() ):
      self.longitude = parseLongitude( iLon[0], iLon[1] )

    if ((type(ilon) == type(float())) or
        (type(ilon) == type(long()))) and ((ilon <= 180) and (ilon >= -180)):
      self.longitude = ilon

    if((type(ilat) == type(long())) or
       (type(ilat) == type(float()))) and ((ilat >= -90) and (ilat <= 90)):
      self.latitude = ilat

  def calculateBearing(self, destination):
    if destination is not GPSPosition:
      return None

    """ calculateBearing - Liefert den Kurswinkel von True (0Grad) zum Ziel

    Die Positionskoordinaten werden im folgenden Format fuer start / destination 
    erwartet: 50.235623167466674  6.4325416563436667

    Basiert ueberwiegend auf den Formeln von der Webseite:
      - http://williams.best.vwh.net/avform.htm#Crs
      - http://www.movable-type.co.uk/scripts/latlong.html"""

    SLat = long()
    SLong = long()
    ZLat = long()
    ZLong = long()

    SLat = math.radians(start[0])
    SLong = math.radians(start[1])
    ZLat = math.radians(destination[0])
    ZLong = math.radians(destination[1])

    # http://williams.best.vwh.net/avform.htm
    y = math.sin( ZLong - SLong ) * math.cos(ZLat)
    x = (math.cos(SLat)*math.sin(ZLat)) - math.sin(SLat)*math.cos(ZLat)*math.cos(ZLong - SLong)

    return ( math.degrees(math.atan2(y,x)) + 360 ) % 360 

  def calculateDistance(self, start, destination):
    """ calculateDistance - Berechnet die Entfernung zweier GPS Punkte in Metern

    Die Positionskoordinaten werden im folgenden Format fuer start / destination 
    erwartet: 50.235623167466674  6.4325416563436667

    URL: http://de.wikipedia.org/wiki/Orthodrome"""

    sf = long()           # Abplattung der Erde
    sa = long(6378137.0)    # Aequatorradius der Erde in Kilometer
    cF = long()
    cG = long()
    sl = long()
    cS = long()           # Bestimmung des groben Abstands D
    cC = long()           # Bestimmung des groben Abstands D
    sw = long()           # Bestimmung des groben Abstands D
    cD = long()           # Abstand D
    cR = long()
    cH1 = long()          # Korrekturfaktor H1
    cH2 = long()          # Korrekturfaktor H2

    sf = 1 / 298.257223563    # WGS84 Referenzellipsoid zugrunde gelegt

    cF = (start[0] + destination[0]) / 2.0
    cG = (start[0] - destination[0]) / 2.0
    sl = (start[1] - destination[1]) / 2.0
    cF = math.radians(cF)
    cG = math.radians(cG)
    sl = math.radians(sl)

    cS =  ((math.sin(cG)**2) * (math.cos(sl)**2)) + ((math.cos(cF)**2)  * (math.sin(sl)**2))
    cC =  ((math.cos(cG)**2) *  (math.cos(sl)**2)) + ((math.sin(cF)**2) * (math.sin(sl)**2))

    sw = math.atan( math.sqrt(cS / cC) )
    cD = (2 * sw * sa)

    cR = math.sqrt(cS * cC) / sw
    cH1 = (3 * cR - 1) / (2 * cC)
    cH2 = (3 * cR + 1) / (2 * cS)

    # Entfernung in Metern
    return cD * (1 + sf * cH1 * (math.sin(cF)**2) * (math.cos(cG)**2) - sf * cH2 * (math.cos(cF)**2) * (math.sin(cG)**2) )



if __name__ == '__main__':
  tt = GPSPosition((5336.3190,"N"),  6.4325416563436667)

