#  _________________________________________________________________________
#
#  PyUtilib: A Python utility library.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  _________________________________________________________________________


__all__ = ['TestCase']

import os
import pyutilib.th
import copy
import pyutilib.subprocess
from coopr.opt import SolverResults
import re
import pyutilib.misc


def _failIfCooprResultsDiffer(self, cmd=None, baseline=None, cwd=None):
    if cwd is not None:
        oldpwd = os.getcwd()
        os.chdir(cwd)
    output = pyutilib.subprocess.run(cmd)
    if output[0] != 0:
        self.fail("Command terminated with nonzero status: '%s'" % cmd)
    results = extract_results( re.split('\n',output[1]) )
    if os.path.exists(baseline):
        INPUT = open(baseline, 'r')
        baseline = "\n".join(INPUT.readlines())
        INPUT.close()
    try:
        compare_results(results, baseline)
    except IOError, err:
        self.fail("Command failed to generate results that can be compared with the baseline: '%s'" % str(err))
    except ValueError, err:
        self.fail("Difference between results and baseline: '%s'" % str(err))


class TestCase(pyutilib.th.TestCase):

    def __init__(self, methodName='runTest'):
        pyutilib.th.TestCase.__init__(self, methodName)

    def failIfCooprResultsDiffer(self, cmd, baseline, cwd=None):
        if not using_yaml:
            self.fail("Cannot compare Coopr results because PyYaml is not installed")
        _failIfCooprresultsDiffer(self, cmd=cmd, baseline=baseline, cwd=cwd)

    def add_coopr_results_test(name=None, cmd=None, fn=None, baseline=None):
        if not using_yaml:
            return
        if cmd is None and fn is None:
            print "ERROR: must specify either the 'cmd' or 'fn' option to define how the output file is generated"
            return
        if name is None and baseline is None:
            print "ERROR: must specify a baseline comparison file, or the test name"
            return
        if baseline is None:
            baseline=name+".txt"
        tmp = name.replace("/","_")
        tmp = tmp.replace("\\","_")
        tmp = tmp.replace(".","_")
        #
        # Create an explicit function so we can assign it a __name__ attribute.
        # This is needed by the 'nose' package
        #
        if fn is None:
            currdir=os.getcwd()
            func = lambda self,c1=currdir,c2=cmd,c3=tmp+".out",c4=baseline: _failIfCooprResultsDiffer(self,cwd=c1,cmd=c2,baseline=c4)
        else:
            # This option isn't implemented...
            sys.exit(1)
            func = lambda self,c1=fn,c2=tmp,c3=baseline: _failIfCooprResultsDiffer(self,fn=c1,name=c2,baseline=c3)
        func.__name__ = "test_"+tmp
        setattr(TestCase, "test_"+tmp, func)
    add_coopr_results_test=staticmethod(add_coopr_results_test)



