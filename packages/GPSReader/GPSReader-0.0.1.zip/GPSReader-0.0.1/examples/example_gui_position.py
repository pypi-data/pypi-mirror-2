# -*- coding: cp1252 -*- 
# $Id: example_gui_position.py 22 2010-04-03 16:51:20Z cfluegel $
from GPSReader import GPSReader
from GPSError import *

from Tkinter import *
import time, thread, sys

class Position:
  def __init__(self):
    self.gpsdev = GPSReader("COM4")

    # TK und Fenster Init 
    self.fenster = Tk()
    self.pos = StringVar()
    self.pos.set("No valid position")
    self.speed = StringVar()
    self.speed.set("No speed")

    self.lpos  = Label(self.fenster, textvariable=self.pos, font=("Arial","36"))
    self.lpos.pack()
    self.lspeed = Label(self.fenster, textvariable=self.speed, font=("Arial","30"))
    self.lspeed.pack()

    self.fenster.bind('<q>', self.quit_event)

    # Thread fuer das aktualisieren
    aktThread = thread.start_new_thread(self.aktualisieren, ())

    # Start die GUI Oberflaeche
    self.fenster.mainloop()

  def quit_event(self,event=None):
    self.gpsdev.stop_thread()
    self.fenster.destroy()
    sys.exit(3)

  def aktualisieren(self):
    print "Thread started" 
    while True:
      print self.gpsdev.isAlive()
      if (not self.gpsdev.isAlive()):
        break

      print "...Thread is running..."
      try:
        temp = self.gpsdev.GGA.getPosition()

        t = "P: |%s| |%s|" % (temp[0], temp[1])
        self.pos.set(t)
      except TypeError:
        print "TypeError Exception caught for pos" 
      except NMEANoValidFix:
        print "The GPS do not have a valid fix"
        self.pos.set("No valid position")

      try:
        temp1 = self.gpsdev.VTG.getSpeed()
        temp2 = self.gpsdev.VTG.getCourse()[0]

        t = "S: %s km/h | C: %s Grad" % (temp1,temp2)
        self.speed.set(t)
      except TypeError:
        print "Exception caught for speed and course" 
      except NMEANoValidFix:
        print "The GPS do not have a valid fix"
        self.speed.set("No valid speed/course")

      time.sleep(3)

    sys.exit(0)

if __name__ == '__main__':
  gui_position = Position()
