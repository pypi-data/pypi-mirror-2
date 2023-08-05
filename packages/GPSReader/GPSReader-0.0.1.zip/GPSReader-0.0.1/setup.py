import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'GPSReader',
    version = '0.0.1',
    description = 'Give access to different NMEA Telegrams of a GPS Receiver',
    author = 'Christoph Fluegel',
    author_email = 'pypi-au-christoph@digitalmonk.de',
    maintainer = 'Christoph Fluegel',
    maintainer_email = 'pypi-ma-christoph@digitalmonk.de',
    url = 'svn://svn.die-starre.de/cfluegel/Python--GPS/trunk/',
    packages= ['GPSReader'],
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Environment :: Win32 (MS Windows)',
      'Environment :: Console',
      'Intended Audience :: Information Technology',
      'Natural Language :: English',
      'Operating System :: Unix',
      'Operating System :: POSIX :: Linux',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.6',
      'Topic :: System :: Networking',
      'Topic :: System :: Hardware'
      ]
)

