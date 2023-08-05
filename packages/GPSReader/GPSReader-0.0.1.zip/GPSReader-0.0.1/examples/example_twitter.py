# -*- coding: cp1252 -*- 
# $Id: example_twitter.py 22 2010-04-03 16:51:20Z cfluegel $
from GPSReader import GPSReader
from GPSError import * 
import time, thread, sys, twitter

# gps
try:
  gpsdev = GPSReader("COM4")
except:
  time.sleep(4)
  sys.exit(1)

# twitter 
tusername = "USERNAME"
tpassword = "PASSWORD"

tapi = twitter.Api(username=tusername, password=tpassword)

startmessage = "example_twitter.py wurde um %i gestartet" % (time.time(),)
print tapi.PostUpdate(startmessage).id

LastUpdate = int(time.time())
while True:
# ############################################################
  fix = False

  try:
    position = gpsdev.GGA.getPosition()
    # More Information: http://mapki.com/wiki/Google_Map_Parameters
    message = "Time: %i | http://maps.google.com/?q=%s,%s&t=m&z=15 " % (time.time(), position[0], position[1])
    status = tapi.PostUpdate(message)
    print "Twitter Msg ID %s" % (status,)

    fix = True
  except TypeError:
    print "TypeError Exception caught for pos"
  except NMEANoValidFix:
    print "The GPS do not have a valid fix (position)"
  except KeyboardInterrupt:
    gpsdev.stop_thread()
    time.sleep(2)
    sys.exit(0)

  # Einige Zeit schlafen, auf Basis der Gefahrenen Gespschwindigkeit 
  if (fix == True):
    try:
      speed = gpsdev.CourseSpeed.getSpeed()
    except:
      speed = -1

    if (speed >= 100):
      time.sleep(60 * 1)
    elif (speed < 100) and (speed >= 50):
      time.sleep(60 * 2.5)
    elif (speed < 50) and (speed >= 10):
      time.sleep(60 * 5)
    else:
      time.sleep(60 * 15)

  else:
    time.sleep(10)
