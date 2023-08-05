from os.path import exists, realpath
from os import system

have_appscript = False
try:
    from appscript import app
    have_appscript = True
except:
    pass

def mate(self):
    frame, lineno = self.stack[self.curindex]
    filename = self.canonic(frame.f_code.co_filename)
    if exists(filename):
        filename = realpath(filename)
        tm_url = 'txmt://open?url=file://%s&line=%d&column=2' % (filename, lineno)
        if have_appscript:
            app("TextMate").get_url(tm_url)
        else:
            system('open %s' % tm_url.replace('&', '\&'))

def preloop(self):
    mate(self)

def precmd(self, line):
    mate(self)
    return line
