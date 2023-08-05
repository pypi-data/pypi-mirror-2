
class Release:
    """
        Release information:
            - name : (str) package name
            - version_info : (tuple<int,int,int,str,int>) The five components of the version number: major, minor, micro, releaselevel, and serial.
            - version : (str) package version in format x.y.z
            - version_description : (str) short description for the current version
            - version_number : (int) x*100 + y*10 + z
            - description : (str) package description
            - long_description : (str) longer package description
            - authors : (dict<str(last name), tuple<str(full name),str(email)>>) package authors
            - url : (str) package url
            - download_url : (str) package download url
            - platform : (seq<str>) list of available platforms
            - keywords : (seq<str>) list of keywords
            - licence : (str) the licence"""
    name = 'PyTango'
    version_info = (7, 1, 1, 'final', 0)
    version = '.'.join(map(str, version_info[:3]))
    version_description = 'This version implements the C++ Tango 7.1 API.'
    version_number = int(version.replace('.',''))
    description = 'A python binding for the Tango control system'
    long_description = 'This module implements the Python Tango Device API mapping'
    license = 'GPL'
    authors = { 'Coutinho' : ('Tiago Coutinho' , 'tcoutinho@cells.es'),
                'Ounsy'    : ('Majid Ounsy',     'majid.ounsy@synchrotron-soleil.fr'),
                'Sune'     : ('Ramon Sune',      'rsune@cells.es'),
                'Taurel'   : ('Emmanuel Taurel', 'taurel@esrf.eu'),
              }
    url = 'http://packages.python.org/PyTango'
    download_url = 'http://pypi.python.org/packages/source/P/PyTango'
    platform = ['Linux', 'Windows XP/2000/NT', 'Windows 95/98/ME']
    keywords = ['Tango', 'CORBA', 'binding']
