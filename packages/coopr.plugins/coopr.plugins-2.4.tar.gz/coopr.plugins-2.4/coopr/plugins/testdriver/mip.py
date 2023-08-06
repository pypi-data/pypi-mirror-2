#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

import os
import os.path
import pyutilib.autotest
import coopr.opt
from pyutilib.component.core import *
import pyutilib.services
from pyutilib.misc import Options

class CooprMIPTestDriver(Plugin):

    implements(pyutilib.autotest.ITestDriver)
    alias('coopr.mip')

    def setUpClass(self, cls, options):
        try:
            cls.pico_convert =  pyutilib.services.registered_executable("pico_convert")
            cls.pico_convert_available= (not cls.pico_convert is None)
        except pyutilib.common.ApplicationError:
            cls.pico_convert_available=False

    def tearDownClass(self, cls, options):
        pass

    def setUp(self, testcase, options):
        global tmpdir
        tmpdir = os.getcwd()
        os.chdir(options.currdir)
        pyutilib.services.TempfileManager.sequential_files(0)
        pyutilib.services.TempfileManager.tempdir = options.currdir
        #
        if ':' in options.solver:
            solver, sub_solver = options.solver.split(':')
            if options.solver_options is None:
                _options = Options()
            else:
                _options = options.solver_options
            _options.solver = sub_solver
            testcase.opt = coopr.opt.SolverFactory(solver, options=_options)
        else:
            testcase.opt = coopr.opt.SolverFactory(options.solver, options=options.solver_options)
        if testcase.opt is None or not testcase.opt.available(False):
            testcase.skipTest('Solver %s is not available' % options.solver)
        else:
            testcase.opt.suffixes = ['.*']

    def tearDown(self, testcase, options):
        global tmpdir
        pyutilib.services.TempfileManager.clear_tempfiles()
        os.chdir(tmpdir)
        pyutilib.services.TempfileManager.unique_files()

    def run_test(self, testcase, name, options):
        #print 'y',name,options.use_pico_convert, testcase.pico_convert_available,
        if options.verbose or options.debug:
            print "Test %s - Running coopr.opt solver with options %s" % (name, str(options))
        if not options.use_pico_convert or (options.use_pico_convert and testcase.pico_convert_available):
            if options.results_format:
                results = testcase.opt.solve(options.currdir+options.files, rformat=coopr.opt.ResultsFormat(options.results_format), logfile=options.currdir+name+".log")
            else:
                results = testcase.opt.solve(options.currdir+options.files, logfile=options.currdir+name+".log")
            baseline = pyutilib.misc.load_yaml( pyutilib.misc.extract_yaml( options.baseline ) )
            if options.tolerance is None:
                tol = 1e-7
            else:
                tol = options.tolerance
            #print 'x',type(repr(results))
            #print 'x',repr(results)
            #print results
            pyutilib.misc.compare_yaml_repn( baseline, results.yaml_repn(), tolerance=tol, exact=False)
        else:
            try:
                if options.results_format:
                    results = testcase.opt.solve(options.currdir+options.files, rformat=coopr.opt.ResultsFormat(options.results_format), logfile=options.currdir+name+".log")
                else:
                    results = testcase.opt.solve(options.currdir+options.files, logfile=options.currdir+name+".log")
            except coopr.opt.ConverterError:
                pass
        if os.path.exists(options.currdir+name+".log"):
            os.remove(options.currdir+name+".log")

