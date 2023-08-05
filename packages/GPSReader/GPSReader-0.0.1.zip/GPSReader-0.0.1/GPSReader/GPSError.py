# $Id: GPSError.py 26 2010-04-03 17:52:24Z cfluegel $ 
class GPSError(Exception):
  """ Generelle GPS Exception """
  def __str__(self):
    return "ERROR: Genereller GPS Error ist aufgetreten!"

#Todo: Delete maybe?
class GPSTelegramMalformed(GPSError):
  def __str__(self):
    return "NMEA Telegramm fehlerhaft!"

#Todo: Delete maybe? 
class GPSCommError(GPSError):
  """ Will be raised if something is wrong with the communication between the
  the software and the connected GPS receiver or if no communciation is possible"""
  def __init__(self,msg=""):
    if msg <> "":
      self._msg = msg
  def __str__(self):
    return self._msg

### new
class NMEATypeError(Exception):
  def __str__(self):
    return "ERROR: Type Fehler!"

class NMEAParseError(Exception):
  def __str__(self):
    return "ERROR: NMEA Telegramm konnte nicht geparst werden!"

class NMEANoValidFix(Exception):
  def __str__(self):
    return "ERROR: No valid position fix!"

if __name__ == "__main__":
  print dir()



