# -*- coding: cp1252 -*-
# $Id: NMEAtelegrams.py 26 2010-04-03 17:52:24Z cfluegel $

# Diese Datei enthaelt alles was fuer die Verarbeitung von NMEA 
# Telegrammen notwendig ist. Neben unterschiedlichen Telegrammen
# gibt es einige Hilfsfunktionen (erster Teil dieser Datei), die so
# zu keiner Klasse passen. 

# Benoetigt fuer alle Fehlermeldung 
from GPSError import *

# Helper Funktionen ausgelagert. So habe ich dann nur noch die 
# eigentlichen Telegramme. 
from NMEAutils import CreateNMEAChkSum, VerifyNMEAChkSum, parseLongitude, parseLatitude

############################################################################
# NMEA Telegramme - Basisklasse
############################################################################
class NMEASentence_Base(object):
  """ Basis Klasse fuer alle NMEA Telegramme """

  def __init__(self):
    self._NMEAFieldList = list()

  def addField(self,field=""):
    """ Fuegt der NMEAFieldListe eines instanzierten Objekts ein weiteres
    Feld hinzu. Ueber diese Liste wird ebenfalls eine NMEA Nachricht
    kontrolliert, da bei einem Fehler die Anzahl nicht identisch ist."""
    # Funktionsnamne eintragen
    # beispiel: NMEAField_Int
    #           NMEAField_Float
    #
    # Derzeit wird einfach nur ein weiteres Feld an die liste angehaengt 
    self._NMEAFieldList.append(field)

  def getFieldList(self):
    """ Liefert die Liste NMEAFieldList zurueck."""
    return self._NMEAFieldList

  def parseSentence(self,NMEAsentence):
    """ Uebergebene NMEA Nachricht wird hier verarbeitet und ebenfalls kontrolliert.
    Sollte die Nachricht falsch aufgebaut sein, dann wird die NMEA Nachricht
    garnicht gelesen."""
    if (NMEAsentence[0] <> "$") or (NMEAsentence[-3] <> "*"):
      raise NMEAParseError

    tmp_sentence = NMEAsentence[7:-3].split(",")
    if len(tmp_sentence) <> len(self._NMEAFieldList):
      raise NMEAParseError

    for field in range(0,len(self._NMEAFieldList)):
      self._NMEAFieldList[field].parseValue(tmp_sentence[field])

  def __getitem__(self,i):
    """ Bei Benutzung von <Objekt>[i] wird genau der Wert aus der NMEAFieldList
    zurueckgegeben."""
    try:
      return self._NMEAFieldList[i].getValue()
    except IndexError:
      return None

  # genereller Output der FieldListe mit vorgehängtem FieldIdentifier
  def __str__(self):
    """ Erstellt aus der NMEAFieldList und dem Part hinter NMEA_ die
    NMEA Nachricht erneut. Zusaetzlich wird noch die Checksumme berechnet,
    da diese nicht in der NMEAFieldList enthalten ist."""
    st = None
    st = "$GP%s," % self.__class__.__name__.split("_")[1]

    for field in range(0,len(self._NMEAFieldList)):
      t = "%s" % self._NMEAFieldList[field].getValue()
      if field <> len(self._NMEAFieldList)-1:
        t = t + ","
      st = st + t
    st = st + "*"
    ChkSum = CreateNMEAChkSum(st)

    return st+ChkSum.upper()

################### NMEA_VTG #########################
class NMEA_VTG(NMEASentence_Base):
  """ NMEA_VTG - Parse the VTG Sentence (COG und SOG information"""
  def __init__(self):
    super(NMEA_VTG, self).__init__()

    self.addField( NMEAField_String() ) # 0. Track Degrees
    self.addField( NMEAField_String() ) # 1. T = True
    self.addField( NMEAField_String() ) # 2. Magnetic track made good
    self.addField( NMEAField_String() ) # 3. M
    self.addField( NMEAField_String() ) # 4. Ground Speed 
    self.addField( NMEAField_String() ) # 5. N = Knots 
    self.addField( NMEAField_String() ) # 6. Ground Speed
    self.addField( NMEAField_String() ) # 7. K = KM/H
    self.addField( NMEAField_String() ) # 8. FAA Mode indicator(Auton.)

  def getCourse(self):
    """ Liefert den letzten empfangenen Kurs vom GPS Geraet"""
    if ( self._NMEAFieldList[8].getValue() <> "A" ):
      return NMEANoValidFix

    try:
      # Liefert degrees und T fuer true
      return (self._NMEAFieldList[0].getValue(), self._NMEAFieldList[1].getValue())
    except:
      raise NMEANoValidFix

  def getSpeed(self,unit="kmh"):
    """ Liefert die letzte bekannte Geschwindigkeit, die vom GPS
    Geraet empfangen worden ist. Default ist KM/H, jedoch kann auf
    knots umgeschaltet werden."""
    if ( self._NMEAFieldList[8].getValue() <> "A"):
      raise NMEANoValidFix

    try:
      if (unit == "kmh"):
        return self._NMEAFieldList[6].getValue()
      else:
        return self._NMEAFieldList[4].getValue()
    except:
      raise NMEANoValidFix

################### NMEA_GGA #########################
class NMEA_GGA(NMEASentence_Base):
  """ NMEA_GGA - Parse the GGA Sentence (Position) """

  def __init__(self):
    super(NMEA_GGA, self).__init__()

    self.addField( NMEAField_String() ) # 0.  time: hhmmss.ss
    self.addField( NMEAField_String() ) # 1.  lat   
    self.addField( NMEAField_String() ) # 2.  n/s
    self.addField( NMEAField_String() ) # 3.  lon
    self.addField( NMEAField_String() ) # 4.  e/w
    self.addField( NMEAField_Int() )    # 5.  0-2 (fix: 1 or 2)
    self.addField( NMEAField_String() ) # 6.  anzahl sateliten: 00-12
    self.addField( NMEAField_String() ) # 7.  hdop
    self.addField( NMEAField_String() ) # 8.  hoehe von der antenne meters 
    self.addField( NMEAField_String() ) # 9.  M 
    self.addField( NMEAField_String() ) # 10. <unknown>
    self.addField( NMEAField_String() ) # 11. M
    self.addField( NMEAField_String() ) # 12. <unknown>
    self.addField( NMEAField_String() ) # 13. dgps stationid

  def _hasFix(self):
    """ Stelle fuer die Klasse eine globale Methode fuer die Pruefung der Gueltigkeit der
    NMEA Nachricht bereit"""
    if (self._NMEAFieldList[5].getValue() > 0 ) and (self._NMEAFieldList[5].getValue() < 6):
      return True

    return False

  def getPosition(self):
    """ Liefert die letzte gueltige GPS Position, die der GPS Empfaenger
    ueber den seriellen Port an den Rechner uebertragen hat."""
    if ( not self._hasFix() ):
      raise NMEANoValidFix

      # Eingebaut, da ich exceptions beim parsen der variablen zu float bekam
    try:
      return ( parseLatitude(self._NMEAFieldList[1].getValue(),self._NMEAFieldList[2].getValue()),
                 parseLongitude(self._NMEAFieldList[3].getValue(),self._NMEAFieldList[4].getValue()) )
    except:
      raise NMEANoValidFix

  def getAntennaHeight(self):
    if ( not self._hasFix() ):
      raise NMEANoValidFix

    return self._NMEAFieldList[8].getValue()

  def getTime(self):
    if ( not self._hasFix() ):
      raise NMEANoValidFix

    return self._NMEAFieldList[0].getValue()

  # Sorgen das in allen Positionsbestimmenden Telegrammen, der selbe Funktionsumfang 
  # vorhanden ist. 
  def getTimeDate(self):
    return None

  def getCourse(self):
    return None

  def getSpeed(self):
    return None

################### NMEA_RMC #########################
class NMEA_RMC(NMEASentence_Base):
  """ NMEA_RMC - Parse the RMC Sentence """

  def __init__(self):
    super(NMEA_RMC, self).__init__()

    self.addField( NMEAField_String() ) # 0. time: hhmmss.ss
    self.addField( NMEAField_String() ) # 1. status: A = VALID
    self.addField( NMEAField_String() ) # 2. latitude 
    self.addField( NMEAField_String() ) # 3. N/S
    self.addField( NMEAField_String() ) # 4. long
    self.addField( NMEAField_String() ) # 5. E/W
    self.addField( NMEAField_String() ) # 6. SOG Knots
    self.addField( NMEAField_String() ) # 7. Track made good, true degrees
    self.addField( NMEAField_String() ) # 8. date: ddmmyy
    self.addField( NMEAField_String() ) # 9. Magnetic variation, degrees
    self.addField( NMEAField_String() ) # 10. E/W
    self.addField( NMEAField_String() ) # 11. FAA mode indicator (N= not valid data, A= autonomous)


  def getPosition(self):
    if (self._NMEAFieldList[1].getValue() <> "A"):
      return NMEANoValidFix

    try:
        return ( parseLatitude(self._NMEAFieldList[2].getValue(),self._NMEAFieldList[3].getValue()), 
                 parseLongitude(self._NMEAFieldList[4].getValue(),self._NMEAFieldList[5].getValue()) )
    except:
      raise NMEANoValidFix

  def getTime(self):
    if (self._NMEAFieldList[1].getValue() <> "A"):
      return NMEANoValidFix
    return self._NMEAFieldList[0].getValue()

  def getTimeDate(self):
    if (self._NMEAFieldList[1].getValue() <> "A"):
      return NMEANoValidFix

    return ( self.getTime(), self._NMEAFieldList[8].getValue() )

  def getCourse(self):
    """ Liefert den letzten empfangenen Kurs vom GPS Geraet"""
    if ( self._NMEAFieldList[1].getValue() <> "A" ):
      return NMEANoValidFix

    try:
      return self._NMEAFieldList[7].getValue()
    except:
      raise NMEANoValidFix

  def getSpeed(self):
    if ( self._NMEAFieldList[1].getValue() <> "A" ):
      return NMEANoValidFix

    return self._NMEAFieldList[6].getValue() * 1.852

  # Sorgen das in allen Positionsbestimmenden Telegrammen, der selbe Funktionsumfang 
  # vorhanden ist. 
  def getAntennaHeight(self):
    return None

############################################################################
# NMEA Field Definitionen. 
############################################################################
class NMEAField_Base():
  def __init__(self):
    self.value = ""

  def getValue(self):
    """ Liefert den gespeicherten Wert des instanzierten Objekts."""
    return self.value

# TODO: Funktioniert, aber es fehlen teilweise die fuehrenden Nullen bei 
# werden wie z.b. die Anzahl der der Satelliten in einer GGA etc. und 
# sonst wo das genutzt wird 
class NMEAField_Int(NMEAField_Base):
  def parseValue(self,value):
    try:
      self.value = int(value)
    except ValueError:
      raise NMEATypeError

class NMEAField_Float(NMEAField_Base):
  def parseValue(self,value):
    self.value = float(value)

class NMEAField_String(NMEAField_Base):
  def parseValue(self,value):
    if ( type(str()) <> type(value) ):
      raise NMEATypeError

    self.value = value



################ TEST #####################################################
if __name__ == '__main__':
  # t1 = NMEA_GGA()
  # t1.parseSentence("$GPGGA,190055.000$GPGGA,190055.000,5336.3190,N,00952.0345,E,0,06,2.2,44.0,M,45.1,")
  # print t1

  # print CreateNMEAChkSum("$GPVTG,199.50,T,,M,0.24,N,0.4,K,N*04")
  # print VerifyNMEAChkSum("$GPVTG,199.50,T,,M,0.24,N,0.4,K,N*04")


  t2 = NMEA_GGA()
  string = "$GPGGA,190055.000,5336.3190,N,00952.0345,E,1,06,2.2,44.0,M,45.1,M,,0000*66"
  t2.parseSentence(string)
  print string
  # print t2.getFieldList()[2].getValue()
  # print t2[2]
  # print t2[12]
  # print t2[5]
  print t2
  print t2.getPosition()
  print t2.getTime()
  print t2.getAntennaHeight()


