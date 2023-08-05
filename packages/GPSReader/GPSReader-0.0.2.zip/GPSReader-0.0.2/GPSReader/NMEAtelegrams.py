# -*- coding: cp1252 -*-
# $Id: NMEAtelegrams.py 34 2010-05-06 19:57:29Z cfluegel $

# This file contains all NMEA telegrams and some helper classes to convert the actual
# NMEA sentences. All NMEA sentences are based on a Base Class which implants some 
# general methodes for all sentences.

# Contains the error exceptions
from GPSError import *

# Some functions which I need seperately or are general useful for other tasks
from NMEAutils import CreateNMEAChkSum, VerifyNMEAChkSum, parseLongitude, parseLatitude
from NMEAutils import GPSPosition

############################################################################
# NMEA Telegram - Baseclasses
############################################################################
class NMEASentence_Base(object):
  """ Base Class for all other NMEA sentences """

  def __init__(self):
    self._NMEAFieldList = list()

  def addField(self,field=""):
    """ Adds a new entry to the internal field list.

    This list will later compared to the NMEA sentence. In case the list have more or less
    fields, one will get an error."""
    self._NMEAFieldList.append(field)

  def getFieldList(self):
    """ returns the field list """
    return self._NMEAFieldList

  def parseSentence(self,NMEAsentence):
    """ parses the sentence and fill the values in the different fields. """
    if (NMEAsentence[0] <> "$") or (NMEAsentence[-3] <> "*"):
      raise NMEAParseError

    tmp_sentence = NMEAsentence[7:-3].split(",")
    if len(tmp_sentence) <> len(self._NMEAFieldList):
      raise NMEAParseError

    for field in range(0,len(self._NMEAFieldList)):
      self._NMEAFieldList[field].parseValue(tmp_sentence[field])

  def __getitem__(self,i):
    """ In case one want to try this object as an array (<Objekt>[i]). """
    try:
      return self._NMEAFieldList[i].getValue()
    except IndexError:
      return None

  def __str__(self):
    """ This method returns the complete object as "valid" NMEA sentence with the Talker $GP.
    The checksum of this sentence will be automatically generated because the chksum of the 
    original message is not saved. """
    st = None
    st = "$GP%s," % self.__class__.__name__.split("_")[1]

    for field in range(0,len(self._NMEAFieldList)):
      t = "%s" % (self._NMEAFieldList[field].getValue())
      if field <> len(self._NMEAFieldList)-1:
        t = t + ","
      st = st + t
    st = st + "*"
    ChkSum = CreateNMEAChkSum(st)

    return st+ChkSum.upper()

################### NMEA_VTG #########################
class NMEA_VTG(NMEASentence_Base):
  """ NMEA_VTG - Parse the VTG Sentence (COG und SOG information)."""
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
    if ( self._NMEAFieldList[8].getValue() <> "A" ):
      raise NMEANoValidFix

    return (self._NMEAFieldList[0].getValue(), self._NMEAFieldList[1].getValue())

  def getSpeed(self,unit="kmh"):
    """ returns the last received speed. The default is in km/h but knots are also possible."""
    if ( self._NMEAFieldList[8].getValue() <> "A"):
      raise NMEANoValidFix

    if (unit == "kmh"):
      return float(self._NMEAFieldList[6].getValue())
    else:
      return float(self._NMEAFieldList[4].getValue())

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
    self.addField( NMEAField_Int(1) ) # 6.  anzahl sateliten: 00-12
    self.addField( NMEAField_String() ) # 7.  hdop
    self.addField( NMEAField_String() ) # 8.  hoehe von der antenne meters 
    self.addField( NMEAField_String() ) # 9.  M 
    self.addField( NMEAField_String() ) # 10. <unknown>
    self.addField( NMEAField_String() ) # 11. M
    self.addField( NMEAField_String() ) # 12. <unknown>
    self.addField( NMEAField_String() ) # 13. dgps stationid

  def _hasFix(self):
    if (self._NMEAFieldList[5].getValue() >= 0 ) and (self._NMEAFieldList[5].getValue() <= 6):
      return True

    return False

  def getPosition(self):
    if ( not self._hasFix() ):
      raise NMEANoValidFix

    return GPSPosition( (self._NMEAFieldList[1].getValue(), self._NMEAFieldList[2].getValue()),
          (self._NMEAFieldList[3].getValue(), self._NMEAFieldList[4].getValue()) )

  def getAntennaHeight(self):
    if ( not self._hasFix() ):
      raise NMEANoValidFix

    return self._NMEAFieldList[8].getValue()

  def getTime(self):
    if ( not self._hasFix() ):
      raise NMEANoValidFix

    return self._NMEAFieldList[0].getValue()

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

    return GPSPosition( (self._NMEAFieldList[2].getValue(), self._NMEAFieldList[3].getValue()),
          (self._NMEAFieldList[4].getValue(), self._NMEAFieldList[5].getValue()) )

  def getTime(self):
    if (self._NMEAFieldList[1].getValue() <> "A"):
      return NMEANoValidFix
    return self._NMEAFieldList[0].getValue()

  def getTimeDate(self):
    if (self._NMEAFieldList[1].getValue() <> "A"):
      return NMEANoValidFix

    return ( self.getTime(), self._NMEAFieldList[8].getValue() )

  def getCourse(self):
    if ( self._NMEAFieldList[1].getValue() <> "A" ):
      return NMEANoValidFix

    return self._NMEAFieldList[7].getValue()

  def getSpeed(self):
    if ( self._NMEAFieldList[1].getValue() <> "A" ):
      return NMEANoValidFix

    return self._NMEAFieldList[6].getValue() * 1.852

############################################################################
# NMEA Field Definitionen. 
############################################################################
class NMEAField_Base(object):
  def __init__(self):
    self.value = ""

  def getValue(self):
    """ returns the value """
    return self.value

# FIXED: Funktioniert, aber es fehlen teilweise die fuehrenden Nullen bei 
# werden wie z.b. die Anzahl der der Satelliten in einer GGA etc. und 
# sonst wo das genutzt wird. Stellen müssen angegeben werden und int muss 
# entsprechend reagieren  
class NMEAField_Int(NMEAField_Base):
  """ NMEAField for Int types. 

  If the value had leading zeros and the field list was configured 
  to acknowledge the leading zeros the return type will be string
  otherwise it will be of type (int)"""
  def __init__(self,leadingZ=0):
    super(NMEAField_Int, self).__init__()

    self.leadingZero = leadingZ

  def parseValue(self,value):
    # In the assumption that the field is always of type 'str' and nothing 
    # else. This is maybe a big ugly hack but it should work around the 
    # oct -> int problem 
    value = value.lstrip("0")
    try:
      self.value = int(value)
    except ValueError:
      raise NMEATypeError

  def getValue(self):
    if self.leadingZero == 0:
      return int(self.value)
    else:
      temp = str(self.value)
      return temp.zfill(len(temp)+self.leadingZero)


class NMEAField_Float(NMEAField_Base):
  def __init__(self):
    super(NMEAField_Float, self).__init__()

  def parseValue(self,value):
    self.value = float(value)

class NMEAField_String(NMEAField_Base):
  def __init__(self):
    super(NMEAField_String, self).__init__()

  def parseValue(self,value):
    if ( type(str()) <> type(value) ):
      raise NMEATypeError

    self.value = value



################ TEST #####################################################
# as before, here are some tests to check the classes and methods of this 
# module file 
if __name__ == '__main__':
  # t1 = NMEA_GGA()
  # t1.parseSentence("$GPGGA,190055.000$GPGGA,190055.000,5336.3190,N,00952.0345,E,0,06,2.2,44.0,M,45.1,")
  # print t1

  print CreateNMEAChkSum("$GPVTG,199.50,T,,M,0.24,N,0.4,K,N*04")
  print VerifyNMEAChkSum("$GPVTG,199.50,T,,M,0.24,N,0.4,K,N*04")


  t2 = NMEA_GGA()

  string = "$GPGGA,190055.000,5336.3190,N,00952.0345,E,1,06,2.2,44.0,M,45.1,M,,0000*66"
  t2.parseSentence(string)
  print "Verifystring %s " % VerifyNMEAChkSum(string)
  print "orig string %s \n" % string
  if string == str(t2):
    print "Teststring is equal with str(t2) (parsed sentence)"
  else:
    print "Teststring and parsed sentence are NOT equal!"
  print "\n"

  print "with getfieldlist: %s" % t2.getFieldList()[0].getValue()
  print "with getitem: %s" % t2[0]
  print "with str: %s " % t2
  print "latitude from class position(): %s " % t2.getPosition().latitude
  print "longitude from class position(): %s " % t2.getPosition().longitude
  print "with gettime(): %s " % t2.getTime()
  print "with getAntennaHeight: %s " % t2.getAntennaHeight()

  t5 = NMEAField_Int(1)
  t5.parseValue("36734")
  print "should be 36734 but with a leading zero: %s " % t5.getValue()
