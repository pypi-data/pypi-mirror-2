#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2009 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________


import sys
import os
from optparse import OptionParser

import pyutilib.services
import textwrap
import traceback
import cProfile
import pstats
import gc

from coopr.pysp.ef import *

from coopr.opt.base import SolverFactory
from coopr.opt.parallel import SolverManagerFactory

#
# utility method to construct an option parser for ef writer arguments
#

def construct_ef_writer_options_parser(usage_string):

   parser = OptionParser()
   parser.add_option("--verbose",
                     help="Generate verbose output, beyond the usual status output. Default is False.",
                     action="store_true",
                     dest="verbose",
                     default=False)
   parser.add_option("--model-directory",
                     help="The directory in which all model (reference and scenario) definitions are stored. Default is \".\".",
                     action="store",
                     dest="model_directory",
                     type="string",
                     default=".")
   parser.add_option("--instance-directory",
                     help="The directory in which all instance (reference and scenario) definitions are stored. Default is \".\".",
                     action="store",
                     dest="instance_directory",
                     type="string",
                     default=".")
   parser.add_option("--generate-weighted-cvar",
                     help="Add a weighted CVaR term to the primary objective",
                     action="store_true",
                     dest="generate_weighted_cvar",
                     default=False)
   parser.add_option("--cvar-weight",
                     help="The weight associated with the CVaR term in the risk-weighted objective formulation. Default is 1.0. If the weight is 0, then *only* a non-weighted CVaR cost will appear in the EF objective - the expected cost component will be dropped.",
                     action="store",
                     dest="cvar_weight",
                     type="float",
                     default=1.0)
   parser.add_option("--risk-alpha",
                     help="The probability threshold associated with cvar (or any future) risk-oriented performance metrics. Default is 0.95.",
                     action="store",
                     dest="risk_alpha",
                     type="float",
                     default=0.95)
   parser.add_option("--output-file",
                     help="Specify the name of the extensive form output file",
                     action="store",
                     dest="output_file",
                     type="string",
                     default="efout.lp")
   parser.add_option("--solve",
                     help="Following write of the extensive form model, solve it.",
                     action="store_true",
                     dest="solve_ef",
                     default=False)
   parser.add_option("--solver",
                     help="The type of solver used to solve scenario sub-problems. Default is cplex.",
                     action="store",
                     dest="solver_type",
                     type="string",
                     default="cplex")
   parser.add_option("--solver-manager",
                     help="The type of solver manager used to coordinate scenario sub-problem solves. Default is serial.",
                     action="store",
                     dest="solver_manager_type",
                     type="string",
                     default="serial")
   parser.add_option("--solver-options",
                     help="Solver options for the extension form problem",
                     action="append",
                     dest="solver_options",
                     type="string",
                     default=[])
   parser.add_option("--mipgap",
                     help="Specifies the mipgap for the EF solve",
                     action="store",
                     dest="mipgap",
                     type="float",
                     default=None)   
   parser.add_option("--output-solver-log",
                     help="Output solver log during the extensive form solve",
                     action="store_true",
                     dest="output_solver_log",
                     default=False)   
   parser.add_option("--profile",
                     help="Enable profiling of Python code.  The value of this option is the number of functions that are summarized.",
                     action="store",
                     dest="profile",
                     default=0)
   parser.add_option("--disable-gc",
                     help="Disable the python garbage collecter. Default is False.",
                     action="store_true",
                     dest="disable_gc",
                     default=False)
   parser.usage=usage_string

   return parser
   
def run_ef_writer(options, args):

   # if the user enabled the addition of the weighted cvar term to the objective,
   # then validate the associated parameters.
   generate_weighted_cvar = False
   cvar_weight = None
   risk_alpha = None

   if options.generate_weighted_cvar is True:

      generate_weighted_cvar = True
      cvar_weight = options.cvar_weight
      risk_alpha = options.risk_alpha

   scenario_tree, binding_instance, scenario_instances = write_ef_from_scratch(os.path.expanduser(options.model_directory),
                                                                               os.path.expanduser(options.instance_directory),
                                                                               os.path.expanduser(options.output_file),
                                                                               options.verbose,
                                                                               generate_weighted_cvar, cvar_weight, risk_alpha)

   if (scenario_tree is None) or (binding_instance is None) or (scenario_instances is None):
      raise RuntimeError, "Failed to write extensive form."      

   if options.solve_ef is True:

      ef_solver = SolverFactory(options.solver_type)
      if ef_solver is None:
         raise ValueError, "Failed to create solver of type="+options.solver_type+" for use in extensive form solve"
      if len(options.solver_options) > 0:
         print "Initializing ef solver with options="+str(options.solver_options)         
         ef_solver.set_options("".join(options.solver_options))
      if options.mipgap is not None:
         if (options.mipgap < 0.0) or (options.mipgap > 1.0):
            raise ValueError, "Value of the mipgap parameter for the EF solve must be on the unit interval; value specified=" + `options.mipgap`
         else:
            ef_solver.mipgap = options.mipgap

      ef_solver_manager = SolverManagerFactory(options.solver_manager_type)
      if ef_solver is None:
         raise ValueError, "Failed to create solver manager of type="+options.solver_type+" for use in extensive form solve"

      print "Queuing extensive form solve"
      ef_action_handle = ef_solver_manager.queue(os.path.expanduser(options.output_file), opt=ef_solver, warmstart=False, tee=options.output_solver_log)
      print "Waiting for extensive form solve"
      ef_results = ef_solver_manager.wait_for(ef_action_handle)
      load_ef_solution(ef_results, binding_instance, scenario_instances)
      scenario_tree.snapshotSolutionFromInstances(scenario_instances)
      print ""
      print "Extensive form solution:"
      scenario_tree.pprintSolution()
      print ""
      print "Extensive form costs:"
      scenario_tree.pprintCosts(scenario_instances)

def run(args=None):

    #
    # Top-level command that executes the extensive form writer.
    # This is segregated from run_ef_writer to enable profiling.
    #

    #
    # Parse command-line options.
    #
    try:
       options_parser = construct_ef_writer_options_parser("runef [options]")
       (options, args) = options_parser.parse_args(args=args)
    except SystemExit:
       # the parser throws a system exit if "-h" is specified - catch
       # it to exit gracefully.
       return

    if options.disable_gc is True:
       gc.disable()
    else:
       gc.enable()

    if options.profile > 0:
        #
        # Call the main ef writer with profiling.
        #
        tfile = pyutilib.services.TempfileManager.create_tempfile(suffix=".profile")
        tmp = cProfile.runctx('run_ef_writer(options,args)',globals(),locals(),tfile)
        p = pstats.Stats(tfile).strip_dirs()
        p.sort_stats('time', 'cum')
        options.profile = eval(options.profile)
        p = p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        p = p.sort_stats('cum','calls')
        p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        p = p.sort_stats('calls')
        p.print_stats(options.profile)
        p.print_callers(options.profile)
        p.print_callees(options.profile)
        pyutilib.services.TempfileManager.clear_tempfiles()
        ans = [tmp, None]
    else:
        #
        # Call the main EF writer without profiling.
        #
        ans = run_ef_writer(options, args)

    gc.enable()
    
    return ans

