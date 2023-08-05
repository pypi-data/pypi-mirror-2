#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

import pyutilib.dev.runtests
import sys
import os.path

def runCooprTests():
    #print os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    #sys.exit(1)
    os.chdir( os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) )
    print "Running tests in directory",os.getcwd()
    if len(sys.argv) == 1:
        dirs=['coopr']
    else:
        dirs=[]
        for dir in sys.argv[1:]:
            if dir.startswith('coopr'):
                dirs.append(dir)
            else:
                dirs.append('coopr.'+dir)
    pyutilib.dev.runtests.run(['runtests','-p','coopr']+dirs)

