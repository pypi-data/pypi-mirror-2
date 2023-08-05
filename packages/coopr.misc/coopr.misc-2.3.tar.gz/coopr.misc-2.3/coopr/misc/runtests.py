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
import optparse

def runCooprTests():
    parser = optparse.OptionParser(usage='test.coopr [options] <dirs>')

    parser.add_option('-d','--dir',
        action='store',
        dest='dir',
        default=None,
        help='Top-level source directory where the tests are applied.')

    options, args = parser.parse_args(sys.argv)

    if options.dir is None:
        os.chdir( os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) )
    else:
        os.chdir( options.dir )

    print "Running tests in directory",os.getcwd()
    options=[]
    if len(args) == 1:
        dirs=['coopr']
    else:
        dirs=[]
        for dir in args:
            if dir.startswith('-'):
                options.append(dir)
            if dir.startswith('coopr'):
                dirs.append(dir)
            else:
                dirs.append('coopr.'+dir)
        if len(dirs) == 0:
            dirs = ['coopr']
    pyutilib.dev.runtests.run(['runtests']+options+['-p','coopr']+dirs)

