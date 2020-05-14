from __future__ import print_function

import re
import subprocess
import warnings
import sys

## Check match the "in" key #
 #
 # params 
 #
 # return 
 # 
 # version 01/2020
 # Author Hiep Nguyen ##
def match_in(key):
    """Is the key  the 'in' keyword"""
    regex = re.compile('^_?([iI][nN])_?$')
    if ( regex.match(key) ):
        return True
    return False







## To key-word arguments #
 #
 # Turn a key dictionary into a list of k=v command-line arguments
 #
 # params 
 #
 # return 
 # 
 # version 01/2020
 # Author Hiep Nguyen ##
def to_kwarg(kwargs):
    ret = []
    for k,v in kwargs.items():
        if( (v == '') or (not v)):
            continue
        # changing keys of dictionary
        if ( match_in(k) ):
            k = 'in'

        if( k == 'threeformat'):
            k ='3format'

        if( k == 'breakk'):
            k = 'break'

        if isinstance(v, list) or isinstance(v, tuple):
            v = ",".join([str(i) for i in v])

        ret.append("%s=%s" % (k,v))

    return ret







def run(f):
    """Wrapper around miriad system calls"""
    def func(*args, **kw):
        if len(args) == 1:
            kw['_in'] = args[0]
        

        if( 'verbose' not in kw ):
            kw['verbose'] = True
        
        verbose = kw.pop('verbose')

        kwarg   = to_kwarg(kw)

        if( f == 'pgflag' ):
            with subprocess.Popen([f]+kwarg, 
                bufsize=0,
                shell=False,
                universal_newlines=True,
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
                stdout, stderr = p.communicate()
                out = stdout.strip()
        else:        
            p = subprocess.Popen([f]+kwarg,
                                 shell=False,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            
            stdout, stderr = p.communicate()
            out = stdout.strip()
            out = out.decode('utf-8')
            if(stderr):
                out = out + '\n' + stderr.decode('utf-8')
        # End - if

        

        if(verbose):
            print( out )

            print('>>> Finished - '+ f)
            print('>\n')

        return out

    return func





## Wrapper class of a Miriad command #
 #
 # params 
 #
 # return 
 # 
 # version 01/2020
 # Author Hiep Nguyen ##
class wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    
    def __getattr__(self, mirfunc):
        f = run(mirfunc)
        f.__name__ = mirfunc
        return f

# This line is required (nice but dirty :-) )
sys.modules[__name__] = wrapper(sys.modules[__name__])