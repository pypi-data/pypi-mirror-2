"""
Support functions for parsing command-line arguments and providing
the Topographica command prompt.  Typically called from the
'./topographica' script, but can be called directly if using
Topographica files within a separate Python.

$Id: commandline.py 11144 2010-07-09 17:55:14Z ceball $
"""
__version__='$Revision: 11144 $'


from optparse import OptionParser

import sys, __main__, math, os, re

import topo
from param.parameterized import Parameterized,OptionalSingleton


try:
    # By default, use a non-GUI backend for matplotlib.
    import matplotlib
    from matplotlib import rcParams
    rcParams['backend']='Agg'
    matplotlib_imported=True
except ImportError:
    matplotlib_imported=False


try:
    import IPython
    ipython_imported=True
except ImportError:
    ipython_imported=False
    print "Note: IPython is not available; using basic interactive Python prompt instead."



# Startup banner
BANNER = """
Welcome to Topographica!

Type help() for interactive help with python, help(topo) for general
information about Topographica, help(commandname) for info on a
specific command, or topo.about() for info on this release, including
licensing information.
"""


class GlobalParams(Parameterized,OptionalSingleton):
    """
    A Parameterized class providing script-level parameters.
    
    Script-level parameters can be set from the commandline by passing
    via -p, e.g. ./topographica -p retina_density=10

    Within scripts, parameters can be declared by using the add()
    method.


    Example usage in a script:

    from topo.misc.commandline import global_params as p
    p.add(
        retina_density=param.Number(default=24.0,bounds=(0,None),
        inclusive_bounds=(False,True),doc=\"""
        The nominal_density to use for the retina.\"""))
    ...
    topo.sim['Retina']=sheet.GeneratorSheet(
        nominal_density=p.retina_density)


    Further information:

    'context' is usually set to __main__.__dict__ and is used to find
    the value of a parameter as it is add()ed to this object
    (i.e. add() has access to values set via the commandline or in
    scripts).

    Values set via set_in_context() or exec_in_context() (used by -p)
    are tracked: warnings are issued for overwritten values, and
    unused values can be warned about via check_for_unused_names().

    The context is not saved in snapshots, but parameter values are
    saved.
    """
    context = None

    def __new__(cls,*args,**kw):
        return OptionalSingleton.__new__(cls,True)

    def __init__(self,context=None,**params):
        self.context = context or {}
        self.unused_names = set()
        params['name']="global_params"
        super(GlobalParams,self).__init__(**params)

    def __getstate__(self):
        # context is neither saved nor restored
        # (in our current usage, the context of the GlobalParams
        # instance will be set to __main__.__dict__ on startup).
        state = super(GlobalParams,self).__getstate__()
        del state['context']
        return state

    def set_in_context(self,**params):
        """
        Set in self.context all name=val pairs specified in **params,
        tracking new names and warning of any replacements.
        """
        for name,val in params.items():
            if name in self.context:
                self.warning("Replacing previous value of '%s' with '%s'"%(name,val))
            self.context[name]=val
            self.unused_names.add(name)
            
    def exec_in_context(self,arg):
        """
        exec arg in self.context, tracking new names and
        warning of any replacements.
        """
        ## contains elaborate scheme to detect what is specified by
        ## -s, and to warn about any replacement
        current_ids = dict([(k,id(v)) for k,v in self.context.items()])

        exec arg in self.context

        for k,v in self.context.items():
            if k in self.unused_names and id(v)!=current_ids[k]:
                self.warning("Replacing previous value of '%s' with '%s'"%(k,v))

        new_names = set(self.context.keys()).difference(set(current_ids.keys()))
        for k in new_names:
            self.unused_names.add(k)
        
    def check_for_unused_names(self):
        """Warn about any unused names."""
        for s in self.unused_names:
            self.warning("'%s' is unused."%s)

# warns for param that specified with -c (but also if name gets defined in __main__,
# e.g. by default_density=global_params.default_density in a script file
##         for name in self.params():
##             if name in self.context:
##                 self.warning("'%s' still exists in global_params.context"%name)

        # detect duplicate param value that wasn't used (e.g. specified with after script)
        for name,val in self.params().items():
            if name in self.context:
                if self.context[name]!=self.inspect_value(name):
                    self.warning("'%s=%s' is unused."%(name,self.context[name]))
            
    
    def add(self,**kw):
        """
        For each parameter_name=parameter_object specified in kw:
        * adds the parameter_object to this object's class
        * if there is an entry in context that has the same name as the parameter,
          sets the value of the parameter in this object to that value, and then removes
          the name from context
        """        
        for p_name,p_obj in kw.items():
            self._add_parameter(p_name,p_obj)
            if p_name in self.context:
                setattr(self,p_name,self.context[p_name])
                if p_name in self.unused_names:
                    # i.e. remove from __main__ if it was a -p option (but not if -c)
                    del self.context[p_name]  
                    self.unused_names.remove(p_name)
                

global_params=GlobalParams(context=__main__.__dict__)



##### Command-prompt formatting
#    
class IPCommandPromptHandler(object):
    """
    Allows control over IPython's dynamic command prompts.
    """
    _format = ''
    _prompt = ''

    @classmethod
    def set_format(cls,format):
        """
        Set IPython's prompt template to format.
        """
        import __main__
        IP = __main__.__dict__['__IP']
        prompt = getattr(IP.outputcache,cls._prompt)
        prompt.p_template = format
        prompt.set_p_str()        
        cls._format = format

    @classmethod
    def get_format(cls):
        """
        Return the current template.
        """
        return cls._format

    
class CommandPrompt(IPCommandPromptHandler):
    """
    Control over input prompt.

    Several predefined formats are provided, and any of these (or any
    arbitrary string) can be used by calling set_format() with their
    values.

    See the IPython manual for details:
    http://ipython.scipy.org/doc/manual/html/config/index.html

    Examples:
      # Use one of the predefined formats:
      CommandPrompt.set_format(CommandPrompt.basic_format)
      # Just print the command number:
      CommandPrompt.set_format('\# ')
      # Print the command number but don't use color:
      CommandPrompt.set_format('\N ')
      # Print the value of my_var at each prompt:
      CommandPrompt.set_format('${my_var}>>> ')        
    """
    _prompt = 'prompt1'
    
    # Predefined alternatives
    basic_format   = 'Topographica>>> '
    simtime_format = 'topo_t${topo.sim.timestr()}>>> '
    simtimecmd_format = 'topo_t${topo.sim.timestr()}_c\\#>>> '
    
    _format = simtimecmd_format


class CommandPrompt2(IPCommandPromptHandler):
    """
    Control over continuation prompt.

    (See CommandPrompt.)
    """
    _prompt = 'prompt2'
    basic_format = '   .\\D.: '
    _format = basic_format


class OutputPrompt(IPCommandPromptHandler):
    """
    Control over output prompt.

    (See CommandPrompt.)
    """
    _prompt = 'prompt_out'
    basic_format = 'Out[\#]:'
    _format = basic_format

#####



# Use to define global constants
global_constants = {'pi':math.pi}

# Create the topographica parser.
usage = "usage: topographica ([<option>]:[<filename>])*\n\
where any combination of options and Python script filenames will be\n\
processed in order left to right."
topo_parser = OptionParser(usage=usage)


def sim_name_from_filename(filename):
    """
    Set the simulation title from the given filename, if none has been
    set already.
    """
    if topo.sim.name is None:
        topo.sim.name=re.sub('.ty$','',os.path.basename(filename))


def boolean_option_action(option,opt_str,value,parser):
    """Callback function for boolean-valued options that apply to the entire run.""" 
    #print "Processing %s" % (opt_str)
    setattr(parser.values,option.dest,True)


def interactive():
    os.environ['PYTHONINSPECT']='1'

# CB: note that topographica should stay open if an error occurs
# anywhere after a -i (i.e. in a -c command or script)
def i_action(option,opt_str,value,parser):
    """Callback function for the -i option."""
    boolean_option_action(option,opt_str,value,parser)
    interactive()
    
topo_parser.add_option("-i","--interactive",action="callback",callback=i_action,
                       dest="interactive",default=False,
                       help="provide an interactive prompt even if stdin does not appear to be a terminal.")


def v_action(option,opt_str,value,parser):
    """Callback function for the -v option."""
    import param.parameterized
    param.parameterized.min_print_level=param.parameterized.VERBOSE
    print "Enabling verbose message output."
    
topo_parser.add_option("-v","--verbose",action="callback",callback=v_action,dest="verbose",default=False,help="""\
enable verbose messaging output.""")


def d_action(option,opt_str,value,parser):
    """Callback function for the -d option."""
    import param.parameterized
    param.parameterized.min_print_level=param.parameterized.DEBUG
    print "Enabling debugging message output."
    
topo_parser.add_option("-d","--debug",action="callback",callback=d_action,dest="debug",default=False,help="""\
enable debugging message output (implies --verbose).""")



def l_action(option,opt_str,value,parser):
    """Callback function for the -l option."""
    boolean_option_action(option,opt_str,value,parser)
    from topo.misc.legacy import install_legacy_support
    print "Enabling legacy support."
    install_legacy_support()
    
topo_parser.add_option("-l","--legacy",action="callback",callback=l_action,dest="legacy",default=False,help="""\
launch Topographica with legacy support enabled.""")


def gui(start=True):
    """Start the GUI as if -g were supplied in the command used to launch Topographica."""
    if matplotlib_imported: 
        from matplotlib import rcParams
        rcParams['backend']='TkAgg'
    auto_import_commands()
    if start:
        import topo.tkgui
        topo.tkgui.start()


# Topographica stays open if an error occurs after -g
# (see comment by i_action)
def g_action(option,opt_str,value,parser):
    """Callback function for the -g option."""
    boolean_option_action(option,opt_str,value,parser)
    interactive()
    gui()


topo_parser.add_option("-g","--gui",action="callback",callback=g_action,dest="gui",default=False,help="""\
launch an interactive graphical user interface; \
equivalent to -c 'from topo.misc.commandline import gui ; gui()'. \
Implies -a.""")


# Keeps track of whether something has been performed, when deciding whether to assume -i
something_executed=False

def c_action(option,opt_str,value,parser):
    """Callback function for the -c option."""
    #print "Processing %s '%s'" % (opt_str,value)
    exec value in __main__.__dict__
    global something_executed
    something_executed=True
            
topo_parser.add_option("-c","--command",action = "callback",callback=c_action,type="string",
		       default=[],dest="commands",metavar="\"<command>\"",
		       help="string of arbitrary Python code to be executed in the main namespace.")



def p_action(option,opt_str,value,parser):
    """Callback function for the -p option."""
    global_params.exec_in_context(value)
    global something_executed
    something_executed=True
            
topo_parser.add_option("-p","--set-parameter",action = "callback",callback=p_action,type="string",
		       default=[],dest="commands",metavar="\"<command>\"",
		       help="command specifying value(s) of script-level (global) Parameter(s).")


def auto_import_commands():
    """Import the contents of all files in the topo/command/ directory."""
    import re,os
    import topo
    import __main__

    # CEBALERT: this kind of thing (topo.__file__) won't work with
    # py2exe and similar tools
    topo_path = os.path.join(os.path.split(topo.__file__)[0],"command")
    for f in os.listdir(topo_path):
        if re.match('^[^_.].*\.py$',f):
            modulename = re.sub('\.py$','',f)
            exec "from topo.command."+modulename+" import *" in __main__.__dict__
    
def a_action(option,opt_str,value,parser):
    """Callback function for the -a option."""
    auto_import_commands()
    
topo_parser.add_option("-a","--auto-import-commands",action="callback",callback=a_action,help="""\
import everything from commands/*.py into the main namespace, for convenience; \
equivalent to -c 'from topo.misc.commandline import auto_import_commands ; auto_import_commands()'.""")



def exec_startup_files():
    """
    Execute startup files, looking at appropriate locations for many different platforms.
    """
    home = os.path.expanduser("~")  # dotfiles on unix
    appdata = os.path.expandvars("$APPDATA") # application data on windows
    appsupport = os.path.join(home,"Library","Application Support") # application support on OS X  

    rcpath = os.path.join(home,'.topographicarc')
    inipath = os.path.join(appdata,'Topographica','topographica.ini')
    configpath = os.path.join(appsupport,'Topographica','topographica.config')

    for startup_file in (rcpath,configpath,inipath):
        if os.path.exists(startup_file):
            print "Executing user startup file %s" % (startup_file)
            execfile(startup_file,__main__.__dict__)
                

    ### Notes about choices for topographica.rc equivalents on different platforms
    #
    ## Windows:
    # Location --  Most programs use the registry or a folder in %appdata% (which is typically
    #  ~\Application Data). The registry is not easily accessible for users, and %appdata% is
    # a hidden folder, which means it doesn't appear in Explorer (or file-open dialogs).
    # Most programs do not have any user-editable configuration files, so this does not matter
    # to them. Maybe we should just use ~\topographica.ini?
    # 
    # Name -- Considered topographica.rc, topographica.dat, topographica.cfg, topographica.ini.
    #  Of those, only .ini is registered as standard in Windows. According to Winows Explorer:
    #  "Files with extension 'INI' are of type 'Configuration Settings'"
    #  Importantly, this means they are already setup to be editable by notepad by default, so
    #  they can be double clicked.
    #
    # http://mail.python.org/pipermail/python-list/2005-September/341702.html
    #
    ## Mac OS:
    # Location -- Seems like programs use either ~/Library/AppName or (more commonly)
    # ~/Library/Application Support/AppName (CEBALERT: is there a var. for that on OS X?).
    # 
    # Name -- there are many different extensions (e.g. dat, config, cfg, ini), none of which
    # opens with any application by default. Some applications use xml.




### Execute what is specified by the options.

def process_argv(argv):
    """
    Process command-line arguments (minus argv[0]!), rearrange and execute.
    """
    # Initial preparation
    import __main__
    for (k,v) in global_constants.items():
        exec '%s = %s' % (k,v) in __main__.__dict__
    
    exec_startup_files()

    # Repeatedly process options, if any, followed by filenames, if any, until nothing is left
    topo_parser.disable_interspersed_args()
    args=argv
    option=None
    global something_executed
    while True:
        # Process options up until the first filename
        (option,args) = topo_parser.parse_args(args,option)

        # Handle filename
        if args:
            filename=args.pop(0)
            #print "Executing %s" % (filename)
            filedir = os.path.dirname(os.path.abspath(filename))
            sys.path.insert(0,filedir) # Allow imports relative to this file's path
            sim_name_from_filename(filename) # Default value of topo.sim.name

            execfile(filename,__main__.__dict__)
            something_executed=True
            
        if not args:
            break

    global_params.check_for_unused_names()

    # If no scripts and no commands were given, pretend -i was given.
    if not something_executed: interactive()
     
    if option.gui: topo.guimain.title(topo.sim.name)

    ## INTERACTIVE SESSION BEGINS HERE (i.e. can't have anything but
    ## some kind of cleanup code afterwards)
    if os.environ.get('PYTHONINSPECT'):
        print BANNER    
        # CB: should probably allow a way for users to pass things to
        # IPython? Or at least set up some kind of topographica ipython
        # config file

        if ipython_imported:
            # Stop IPython namespace hack?
            # http://www.nabble.com/__main__-vs-__main__-td14606612.html
            __main__.__name__="__mynamespace__"

            from IPython.Shell import IPShell

            IPShell(['-noconfirm_exit','-nobanner',
                     '-pi1',CommandPrompt.get_format(),
                     '-pi2',CommandPrompt2.get_format(),
                     '-po',OutputPrompt.get_format()],
                    user_ns=__main__.__dict__).mainloop(sys_exit=1)            

        

