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
import pyutilib.misc
import textwrap
import traceback

# garbage collection control.
import gc

# for profiling
import cProfile
import pstats

# for serializing
import pickle

from coopr.pysp.convergence import *
from coopr.pysp.scenariotree import *
from coopr.pysp.ph import *
from coopr.pysp.ef import *
from coopr.opt.base import SolverFactory
from coopr.opt.parallel import SolverManagerFactory

#
# utility method to construct an option parser for ph arguments, to be
# supplied as an argument to the runph method.
#

def construct_ph_options_parser(usage_string):

   parser = OptionParser()
   parser.add_option("--verbose",
                     help="Generate verbose output for both initialization and execution. Default is False.",
                     action="store_true",
                     dest="verbose",
                     default=False)
   parser.add_option("--report-solutions",
                     help="Always report PH solutions after each iteration. Enabled if --verbose is enabled. Default is False.",
                     action="store_true",
                     dest="report_solutions",
                     default=False)
   parser.add_option("--report-weights",
                     help="Always report PH weights prior to each iteration. Enabled if --verbose is enabled. Default is False.",
                     action="store_true",
                     dest="report_weights",
                     default=False)
   parser.add_option("--report-only-statistics",
                     help="When reporting solutions (if enabled), only output per-variable statistics - not the individual scenario values. Default is False.",
                     action="store_true",
                     dest="report_only_statistics",
                     default=False)
   parser.add_option("--output-scenario-tree-solution",
                     help="Report the full solution (even leaves) in scenario tree format upon termination. Values represent averages, so convergence is not an issue. Default is False.",
                     action="store_true",
                     dest="output_scenario_tree_solution",
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
   parser.add_option("--scenario-solver-options",
                     help="Solver options for all PH scenario sub-problems",
                     action="append",
                     dest="scenario_solver_options",
                     type="string",
                     default=[])
   parser.add_option("--scenario-mipgap",
                     help="Specifies the mipgap for all PH scenario sub-problems",
                     action="store",
                     dest="scenario_mipgap",
                     type="float",
                     default=None)
   parser.add_option("--ef-solver-options",
                     help="Solver options for the extension form problem",
                     action="append",
                     dest="ef_solver_options",
                     type="string",
                     default=[])
   parser.add_option("--ef-mipgap",
                     help="Specifies the mipgap for the EF solve",
                     action="store",
                     dest="ef_mipgap",
                     type="float",
                     default=None)
   parser.add_option("--max-iterations",
                     help="The maximal number of PH iterations. Default is 100.",
                     action="store",
                     dest="max_iterations",
                     type="int",
                     default=100)
   parser.add_option("--default-rho",
                     help="The default (global) rho for all blended variables. Default is 1.",
                     action="store",
                     dest="default_rho",
                     type="float",
                     default=1.0)
   parser.add_option("--rho-cfgfile",
                     help="The name of a configuration script to compute PH rho values. Default is None.",
                     action="store",
                     dest="rho_cfgfile",
                     type="string",
                     default=None)
   parser.add_option("--bounds-cfgfile",
                     help="The name of a configuration script to set variable bound values. Default is None.",
                     action="store",
                     dest="bounds_cfgfile",
                     default=None)
   parser.add_option("--enable-termdiff-convergence",
                     help="Terminate PH based on the termdiff convergence metric. Default is True.",
                     action="store_true",
                     dest="enable_termdiff_convergence",
                     default=True)
   parser.add_option("--enable-normalized-termdiff-convergence",
                     help="Terminate PH based on the normalized termdiff convergence metric. Default is True.",
                     action="store_true",
                     dest="enable_normalized_termdiff_convergence",
                     default=False)
   parser.add_option("--termdiff-threshold",
                     help="The convergence threshold used in the term-diff and normalized term-diff convergence criteria. Default is 0.01.",
                     action="store",
                     dest="termdiff_threshold",
                     type="float",
                     default=0.01)
   parser.add_option("--enable-free-discrete-count-convergence",
                     help="Terminate PH based on the free discrete variable count convergence metric. Default is False.",
                     action="store_true",
                     dest="enable_free_discrete_count_convergence",
                     default=False)
   parser.add_option("--free-discrete-count-threshold",
                     help="The convergence threshold used in the criterion based on when the free discrete variable count convergence criterion. Default is 20.",
                     action="store",
                     dest="free_discrete_count_threshold",
                     type="float",
                     default=20)
   parser.add_option("--enable-ww-extensions",
                     help="Enable the Watson-Woodruff PH extensions plugin. Default is False.",
                     action="store_true",
                     dest="enable_ww_extensions",
                     default=False)
   parser.add_option("--ww-extension-cfgfile",
                     help="The name of a configuration file for the Watson-Woodruff PH extensions plugin. Default is wwph.cfg.",
                     action="store",
                     dest="ww_extension_cfgfile",
                     type="string",
                     default="")
   parser.add_option("--ww-extension-suffixfile",
                     help="The name of a variable suffix file for the Watson-Woodruff PH extensions plugin. Default is wwph.suffixes.",
                     action="store",
                     dest="ww_extension_suffixfile",
                     type="string",
                     default="")
   parser.add_option("--user-defined-extension",
                     help="The name of a python module specifying a user-defined PH extension plugin.",
                     action="store",
                     dest="user_defined_extension",
                     type="string",
                     default=None)
   parser.add_option("--write-ef",
                     help="Upon termination, write the extensive form of the model - accounting for all fixed variables.",
                     action="store_true",
                     dest="write_ef",
                     default=False)
   parser.add_option("--solve-ef",
                     help="Following write of the extensive form model, solve it.",
                     action="store_true",
                     dest="solve_ef",
                     default=False)
   parser.add_option("--ef-output-file",
                     help="The name of the extensive form output file (currently only LP format is supported), if writing of the extensive form is enabled. Default is efout.lp.",
                     action="store",
                     dest="ef_output_file",
                     type="string",
                     default="efout.lp")
   parser.add_option("--suppress-continuous-variable-output",
                     help="Eliminate PH-related output involving continuous variables.",
                     action="store_true",
                     dest="suppress_continuous_variable_output",
                     default=False)
   parser.add_option("--keep-solver-files",
                     help="Retain temporary input and output files for scenario sub-problem solves",
                     action="store_true",
                     dest="keep_solver_files",
                     default=False)
   parser.add_option("--output-solver-logs",
                     help="Output solver logs during scenario sub-problem solves",
                     action="store_true",
                     dest="output_solver_logs",
                     default=False)
   parser.add_option("--output-ef-solver-log",
                     help="Output solver log during the extensive form solve",
                     action="store_true",
                     dest="output_ef_solver_log",
                     default=False)
   parser.add_option("--output-solver-results",
                     help="Output solutions obtained after each scenario sub-problem solve",
                     action="store_true",
                     dest="output_solver_results",
                     default=False)
   parser.add_option("--output-times",
                     help="Output timing statistics for various PH components",
                     action="store_true",
                     dest="output_times",
                     default=False)
   parser.add_option("--disable-warmstarts",
                     help="Disable warm-start of scenario sub-problem solves in PH iterations >= 1. Default is False.",
                     action="store_true",
                     dest="disable_warmstarts",
                     default=False)
   parser.add_option("--drop-proximal-terms",
                     help="Eliminate proximal terms (i.e., the quadratic penalty terms) from the weighted PH objective. Default is False.",
                     action="store_true",
                     dest="drop_proximal_terms",
                     default=False)
   parser.add_option("--retain-quadratic-binary-terms",
                     help="Do not linearize PH objective terms involving binary decision variables",
                     action="store_true",
                     dest="retain_quadratic_binary_terms",
                     default=False)
   parser.add_option("--linearize-nonbinary-penalty-terms",
                     help="Approximate the PH quadratic term for non-binary variables with a piece-wise linear function, using the supplied number of equal-length pieces from each bound to the average",
                     action="store",
                     dest="linearize_nonbinary_penalty_terms",
                     type="int",
                     default=0)
   parser.add_option("--breakpoint-strategy",
                     help="Specify the strategy to distribute breakpoints on the [lb, ub] interval of each variable when linearizing. 0 indicates uniform distribution. 1 indicates breakpoints at the node min and max, uniformly in-between. 2 indicates more aggressive concentration of breakpoints near the observed node min/max.",
                     action="store",
                     dest="breakpoint_strategy",
                     type="int",
                     default=0)
   parser.add_option("--checkpoint-interval",
                     help="The number of iterations between writing of a checkpoint file. Default is 0, indicating never.",
                     action="store",
                     dest="checkpoint_interval",
                     type="int",
                     default=0)
   parser.add_option("--restore-from-checkpoint",
                     help="The name of the checkpoint file from which PH should be initialized. Default is \"\", indicating no checkpoint restoration",
                     action="store",
                     dest="restore_from_checkpoint",
                     type="string",
                     default="")
   parser.add_option("--profile",
                     help="Enable profiling of Python code.  The value of this option is the number of functions that are summarized.",
                     action="store",
                     dest="profile",
                     type="int",
                     default=0)
   parser.add_option("--disable-gc",
                     help="Disable the python garbage collecter. Default is False.",
                     action="store_true",
                     dest="disable_gc",
                     default=False)

   parser.usage=usage_string

   return parser

#
# Create the reference model / instance and scenario tree instance for PH.
#

def load_reference_and_scenario_models(options):

   #
   # create and populate the reference model/instance pair.
   #

   reference_model = None
   reference_instance = None

   try:
      reference_model_filename = os.path.expanduser(options.model_directory)+os.sep+"ReferenceModel.py"
      if options.verbose is True:
         print "Scenario reference model filename="+reference_model_filename
      model_import = pyutilib.misc.import_file(reference_model_filename)
      if "model" not in dir(model_import):
         print ""
         print "***ERROR: Exiting test driver: No 'model' object created in module "+reference_model_filename
         return None, None, None, None

      if model_import.model is None:
         print ""
         print "***ERROR: Exiting test driver: 'model' object equals 'None' in module "+reference_model_filename
         return None, None, None, None
 
      reference_model = model_import.model
   except IOError:
      print "***ERROR: Failed to load scenario reference model from file="+reference_model_filename
      return None, None, None, None

   try:
      reference_instance_filename = os.path.expanduser(options.instance_directory)+os.sep+"ReferenceModel.dat"
      if options.verbose is True:
         print "Scenario reference instance filename="+reference_instance_filename
      reference_instance = reference_model.create(reference_instance_filename)
   except IOError:
      print "***ERROR: Failed to load scenario reference instance data from file="+reference_instance_filename
      return None, None, None, None

   #
   # create and populate the scenario tree model
   #

   from coopr.pysp.util.scenariomodels import scenario_tree_model
   scenario_tree_instance = None

   try:
      scenario_tree_instance_filename = os.path.expanduser(options.instance_directory)+os.sep+"ScenarioStructure.dat"
      if options.verbose is True:
         print "Scenario tree instance filename="+scenario_tree_instance_filename
      scenario_tree_instance = scenario_tree_model.create(scenario_tree_instance_filename)
   except IOError:
      print "***ERROR: Failed to load scenario tree reference instance data from file="+scenario_tree_instance_filename
      return None, None, None, None
   
   #
   # construct the scenario tree
   #
   scenario_tree = ScenarioTree(scenarioinstance=reference_instance,
                                scenariotreeinstance=scenario_tree_instance)

   return reference_model, reference_instance, scenario_tree, scenario_tree_instance

#
# Create a PH object from a checkpoint.
#
def create_ph_from_checkpoint(options):

   # we need to load the reference model, as pickle doesn't save contents of .py files!
   try:
      reference_model_filename = os.path.expanduser(options.model_directory)+os.sep+"ReferenceModel.py"
      if options.verbose is True:
         print "Scenario reference model filename="+reference_model_filename
      model_import = pyutilib.misc.import_file(reference_model_filename)
      if "model" not in dir(model_import):
         print "***ERROR: Exiting test driver: No 'model' object created in module "+reference_model_filename
         return

      if model_import.model is None:
         print "***ERROR: Exiting test driver: 'model' object equals 'None' in module "+reference_model_filename
         return None
 
      reference_model = model_import.model
   except IOError:
      print "***ERROR: Failed to load scenario reference model from file="+reference_model_filename
      return None

   # import the saved state
      
   try:
      checkpoint_file = open(options.restore_from_checkpoint,"r")
      ph = pickle.load(checkpoint_file)
      checkpoint_file.close()
      
   except IOError, msg:
      raise RuntimeError, msg

   # tell PH to build the right solver manager and solver TBD - AND PLUGINS, BUT LATER

   raise RuntimeError, "Checkpoint restoration is not fully supported/tested yet!"

   return ph

#
# Create a PH object from a checkpoint.
#
def create_ph_from_scratch(options, reference_model, reference_instance, scenario_tree):

   #
   # print the input tree for validation/information purposes.
   #
   if options.verbose is True:
      scenario_tree.pprint()

   #
   # validate the tree prior to doing anything serious
   #
   print ""
   if scenario_tree.validate() is False:
      print "***ERROR: Scenario tree is invalid****"
      return None
   else:
      if options.verbose is True:
         print "Scenario tree is valid!"
   print ""

   #
   # if any of the ww extension configuration options are specified without the 
   # ww extension itself being enabled, halt and warn the user - this has led
   # to confusion in the past, and will save user support time.
   #
   if len(options.ww_extension_cfgfile) > 0 and options.enable_ww_extensions is False:
      print "***ERROR: A configuration file was specified for the WW extension module, but the WW extensions are not enabled!"
      return None

   if len(options.ww_extension_suffixfile) > 0 and options.enable_ww_extensions is False:
      print "***ERROR: A suffix file was specified for the WW extension module, but the WW extensions are not enabled!"         
      return None

   #
   # if a breakpoint strategy is specified without linearization eanbled, halt and warn the user.
   #
   if (options.breakpoint_strategy > 0) and (options.linearize_nonbinary_penalty_terms == 0):
      print "***ERROR: A breakpoint distribution strategy was specified, but linearization is not enabled!"
      return None

   #
   # deal with any plugins. ww extension comes first currently, followed by an option user-defined plugin.
   # order only matters if both are specified.
   #
   if options.enable_ww_extensions is True:

      from coopr.pysp import wwphextension

      plugin = ExtensionPoint(IPHExtension)
      if len(options.ww_extension_cfgfile) > 0:
         plugin.service()._configuration_filename = options.ww_extension_cfgfile
      if len(options.ww_extension_suffixfile) > 0:
         plugin.service()._suffix_filename = options.ww_extension_suffixfile

   if options.user_defined_extension is not None:
      print "Trying to import user-defined PH extension module="+options.user_defined_extension
      # JPW removed the exception handling logic, as the module importer
      # can raise a broad array of exceptions. 
      __import__(options.user_defined_extension)
      print "Module successfully loaded"

   #
   # construct the convergence "computer" class.
   #
   converger = None
   # go with the non-defaults first, and then with the default.
   if options.enable_free_discrete_count_convergence is True:
      converger = NumFixedDiscreteVarConvergence(convergence_threshold=options.free_discrete_count_threshold)
   elif options.enable_normalized_termdiff_convergence is True:
      converger = NormalizedTermDiffConvergence(convergence_threshold=options.termdiff_threshold)      
   else:
      converger = TermDiffConvergence(convergence_threshold=options.termdiff_threshold)      

   
   #
   # construct and initialize PH
   #
   ph = ProgressiveHedging(max_iterations=options.max_iterations, \
                           rho=options.default_rho, \
                           rho_setter=options.rho_cfgfile, \
                           bounds_setter=options.bounds_cfgfile, \
                           solver=options.solver_type, \
                           solver_manager=options.solver_manager_type, \
                           output_scenario_tree_solution=options.output_scenario_tree_solution, \
                           scenario_solver_options=options.scenario_solver_options, \
                           scenario_mipgap=options.scenario_mipgap, \
                           keep_solver_files=options.keep_solver_files, \
                           output_solver_log=options.output_solver_logs, \
                           output_solver_results=options.output_solver_results, \
                           verbose=options.verbose, \
                           report_solutions=options.report_solutions, \
                           report_weights=options.report_weights, \
                           report_only_statistics=options.report_only_statistics, \
                           output_times=options.output_times, \
                           disable_warmstarts=options.disable_warmstarts,
                           drop_proximal_terms=options.drop_proximal_terms,
                           retain_quadratic_binary_terms=options.retain_quadratic_binary_terms, \
                           linearize_nonbinary_penalty_terms=options.linearize_nonbinary_penalty_terms, \
                           breakpoint_strategy=options.breakpoint_strategy, \
                           checkpoint_interval=options.checkpoint_interval)

   ph.initialize(scenario_data_directory_name=os.path.expanduser(options.instance_directory), \
                 model=reference_model, \
                 model_instance=reference_instance, \
                 scenario_tree=scenario_tree, \
                 converger=converger)

   if options.suppress_continuous_variable_output is True:
      ph._output_continuous_variable_stats = False # clutters up the screen, when we really only care about the binaries.

   return ph

#
# Given a PH object, execute it and optionally solve the EF at the end.
#

def run_ph(options, ph):

   #
   # at this point, we have an initialized PH object by some means.
   #
   start_time = time.time()

   #
   # kick off the solve
   #
   ph.solve()

   end_time = time.time()

   print ""
   print "Total PH execution time=%8.2f seconds" %(end_time - start_time)
   print ""
   if options.output_times is True:
      ph.print_time_stats()

   #
   # write the extensive form, accounting for any fixed variables.
   #
   if (options.write_ef is True) or (options.solve_ef is True):
      print ""
      print "Writing EF for remainder problem"
      print ""
      create_and_write_ef(ph._scenario_tree, ph._instances, os.path.expanduser(options.ef_output_file))

   #
   # solve the extensive form.
   #
   if options.solve_ef is True:
      print ""
      print "Solving extensive form written to file="+os.path.expanduser(options.ef_output_file)
      print ""

      ef_solver = SolverFactory(options.solver_type)
      if ef_solver is None:
         raise ValueError, "Failed to create solver of type="+options.solver_type+" for use in extensive form solve"
      if len(options.ef_solver_options) > 0:
         print "Initializing ef solver with options="+str(options.ef_solver_options)         
         ef_solver.set_options("".join(options.ef_solver_options))
      if options.ef_mipgap is not None:
         if (options.ef_mipgap < 0.0) or (options.ef_mipgap > 1.0):
            raise ValueError, "Value of the mipgap parameter for the EF solve must be on the unit interval; value specified=" + `options.ef_mipgap`
         else:
            ef_solver.mipgap = options.ef_mipgap

      ef_solver_manager = SolverManagerFactory(options.solver_manager_type)
      if ef_solver is None:
         raise ValueError, "Failed to create solver manager of type="+options.solver_type+" for use in extensive form solve"

      print "Queuing extensive form solve"
      ef_action_handle = ef_solver_manager.queue(os.path.expanduser(options.ef_output_file), opt=ef_solver, warmstart=False, tee=options.output_ef_solver_log)
      print "Waiting for extensive form solve"
      ef_results = ef_solver_manager.wait_for(ef_action_handle)
      print "Extensive form solve results:"
      ef_results.write(num=1)
   
#
# The main PH initialization / runner routine.
#

def exec_ph(options):

   ph = None

   # if we are restoring from a checkpoint file, do so - otherwise, construct PH from scratch.
   if len(options.restore_from_checkpoint) > 0:

      ph = create_ph_from_checkpoint(options)
      
   else:

      reference_model, reference_instance, scenario_tree, scenario_tree_instance = load_reference_and_scenario_models(options)
      if reference_model is None or reference_instance is None or scenario_tree is None:
         return
      ph = create_ph_from_scratch(options, reference_model, reference_instance, scenario_tree)

   if ph is None:
      print "***FAILED TO CREATE PH OBJECT"
      return

   run_ph(options, ph)

def run(args=None):

    #
    # Top-level command that executes the extensive form writer.
    # This is segregated from run_ef_writer to enable profiling.
    #

    #
    # Parse command-line options.
    #
    try:
       ph_options_parser = construct_ph_options_parser("runph [options]")
       (options, args) = ph_options_parser.parse_args(args=args)
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
        # Call the main PH routine with profiling.
        #
        tfile = pyutilib.services.TempfileManager.create_tempfile(suffix=".profile")
        tmp = cProfile.runctx('exec_ph(options)',globals(),locals(),tfile)
        p = pstats.Stats(tfile).strip_dirs()
        p.sort_stats('time', 'cum')
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
        # Call the main PH routine without profiling.
        #
        ans = exec_ph(options)

    gc.enable()
    
    return ans
