import atexit
import sys
import urllib2

ENDPOINT = 'http://buildthreat.appspot.com'

BLACK = '\033[40m'
RED = '\033[41m'
MAGENTA = '\033[45m'
YELLOW = '\033[43m'
BLUE = '\033[44m'
GREEN = '\033[42m'
BGRESET = '\033[49m'

FGWHITE = '\033[37m'
FGRESET = '\033[39m'

LEVELS = [
    (5, 'Severe', RED),
    (4, 'High', MAGENTA),
    (3, 'Elevated', YELLOW),
    (2, 'Guarded', BLUE),
    (1, 'Low', GREEN),
    ]

def phone_home(success=True):
    try:
        urllib2.urlopen(ENDPOINT + '/?result=' + (success and '1' or '0'))
    except:
        pass

def patch_sysexit(old_sysexit):
    def sysexit(*args, **kw):
        success = not len(args) or not args[0]
        phone_home(success)
        old_sysexit(*args, **kw)
    return sysexit

def install(buildout):

    atexit.register(phone_home)
    # eeeeevil
    sys.exit = patch_sysexit(sys.exit)

    try:
        level = int(urllib2.urlopen(ENDPOINT + '/level').read())
        level = LEVELS[5-level]
    except:
        return

    print '---------------------------------------------------------'
    print 'The current global buildout threat level is:',
    print level[2] + '  ' + FGWHITE + level[1].upper() + FGRESET + '  ' + BGRESET
    print '---------------------------------------------------------'
