#! python
import ConfigParser
import sys, os, string

def setup_config(inipath):
    config = ConfigParser.RawConfigParser()
    config.read(inipath)
    if not config.has_section('PBoptions'):
        config.add_section('PBoptions')
    if not config.has_option('PBoptions', 'workingdir'):
        config.set('PBoptions', 'workingdir', os.getcwd())
    if not config.has_option('PBoptions', 'default_bibliography'):
        config.set('PBoptions', 'default_bibliography', os.path.join(sysdir, 'library.bib'))
    if not config.has_option('PBoptions', 'exclude_by_default'):
        config.set('PBoptions', 'exclude_by_default', 'submissions')
    if not config.has_option('PBoptions', 'default_bibtex_entry_type'):
        config.set('PBoptions', 'default_bibtex_entry_type', 'Misc')
    if not config.has_option('PBoptions', 'default_bibtex_entry_style'):
        config.set('PBoptions', 'default_bibtex_entry_style', '0')
    if not config.has_option('PBoptions', 'default_bibtex_url_handling'):
        config.set('PBoptions', 'default_bibtex_url_handling', 'href_howpublished')
    if not config.has_option('PBoptions', 'export_tsv'):
        config.set('PBoptions', 'export_tsv', 'false')
    config.write(open(inipath, 'w'))
    return config

def GetAppdir():
    '''get the directory of the application itself'''
    if not __file__:
        pathname = sys.argv[0]
        retval = os.path.split(os.path.abspath(pathname))[0]
    else:
        retval = os.path.dirname(__file__)
    return retval

print 'appdir - ', GetAppdir()
APPNAME = "pieberry"
if sys.platform == 'linux2':
    sysdir = os.path.join(os.environ["HOME"], "".join([".", APPNAME]))
elif sys.platform == 'win32':
    if os.path.exists(os.path.join(os.environ["HOMEPATH"], "Application Data")):
        sysdir = os.path.join(os.environ["HOMEPATH"], "Application Data", APPNAME)
    else:
        sysdir = os.getcwd()
else: 
    sysdir = os.getcwd()
if not os.path.exists(sysdir):
    os.mkdir(sysdir)
inipath = os.path.join(sysdir, 'pieberry.ini')
config = setup_config(inipath)
DEFAULT_BIBLIOGRAPHY = config.get('PBoptions', 'default_bibliography')
if not (os.path.exists(config.get('PBoptions', 'workingdir')) and os.path.isdir(config.get('PBoptions', 'workingdir'))):
    os.mkdir(config.get('PBoptions', 'workingdir'))
if not os.path.exists(DEFAULT_BIBLIOGRAPHY):
    a = open(DEFAULT_BIBLIOGRAPHY, 'w')
    a.write(' ')
    a.close()
exclude_by_default = string.split(config.get('PBoptions', 'exclude_by_default'), ',')
PY2EXE = False
if PY2EXE:
    IMGDIR = os.getcwd()
else:
    IMGDIR = GetAppdir()

try:
    from pieberry_pybtex import *
    PYBTEX = True
    print 'Pybtex in use'
except:
    PYBTEX = False
    
try:
    import pynotify
    if pynotify.init(APPNAME):
        PYNOTIFY = True
    else:
        PYNOTIFY = False
except:
    PYNOTIFY = False

ENTRY_TYPE_CHOICES = {0: '@Misc with url field', 
                      1: '@Misc with \url{} in howpublished',
                      2: '@Misc with \href{} in howpublished', 
                      3: '@Online (biblatex only)'
                      }
ENTRY_TYPE_KEYS = {0: 'Misc',
                   1: 'Misc',
                   2: 'Misc',
                   3: 'Online',
                   }

    


