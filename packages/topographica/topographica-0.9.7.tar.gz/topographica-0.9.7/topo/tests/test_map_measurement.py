"""
Functions to test that map measurements haven't changed.

Use generate() to save data, and test() to check that the data is
unchanged in a later version. Results from generate() are already
checked into svn, so intentional changes to map measurement mean new
data must be generated and committed. E.g.

# ...deliberate change to orientation map measurement...
$ ./topographica -c 'default_density=8' examples/lissom_oo_or.ty -c \
  'topo.sim.run(100)' -c \
  'from topo.tests.test_map_measurement import *' -c \
  'generate(["Orientation Preference"])'
# now commit the resulting data file to the svn repository


plotgroups_to_test is a list of PlotGroups for which these
test functions are expected to be useful.
"""

import pickle

from numpy.testing import assert_array_almost_equal

import topo

from param import resolve_path, normalize_path
from topo.command.analysis import *
from topo.command.pylabplot import *
from topo.plotting.plotgroup import plotgroups

# CEBALERT: change to be the all-in-one model eventually, and
# uncomment all ocular/disparity/direction groups below.
sim_name = 'lissom_oo_or'

# CEB: tests should store params of commands
# so we don't have to update data if someone
# e.g. edits a default value.

plotgroups_to_test = [
    # Several plotgroups are commented out because I was only thinking
    # about map measurement that results in sheet_views stored for V1.
    # (All could be included if the functions below were to be
    # extended to handle sheets other than V1, etc.)
    #'Activity',
    #'Connection Fields',
    #'Projection',
    #'Projection Activity',
    #'RF Projection',
    #'RF Projection (noise)',

    'Position Preference',
    # 'Center of Gravity',
    # 'Orientation and Ocular Preference',
    # 'Orientation and Direction Preference',
    # 'Orientation, Ocular and Direction Preference',
    'Orientation Preference',
    #'Ocular Preference',
    'Spatial Frequency Preference',
    #'PhaseDisparity Preference',
    'Orientation Tuning Fullfield',
    'Orientation Tuning',
    'Size Tuning',
    'Contrast Response',
    #'Retinotopy',  commented out because measurement is unstable
    #'Direction Preference',
    'Corner OR Preference'
    ]


def _reset_views(sheet):
    if hasattr(sheet,'sheet_views'):
        sheet.sheet_views = {}
    if hasattr(sheet,'curve_dict'):
        sheet.curve_dict = {}
    

def generate(plotgroup_names):
    assert topo.sim.name==sim_name
    assert topo.sim['V1'].nominal_density==8
    assert topo.sim.time()==100

    for name in plotgroup_names:
        print "* Generating data for plotgroups['%s']"%name

        views = {}
        sheet = topo.sim['V1']

        _reset_views(sheet)

        plotgroups[name]._exec_pre_plot_hooks()

        sheets_views = views[sheet.name] = {}

        if hasattr(sheet,'sheet_views'):
            sheets_views['sheet_views'] = sheet.sheet_views
        if hasattr(sheet,'curve_dict'):
            sheets_views['curve_dict'] = sheet.curve_dict

        f = open(normalize_path('tests/%s_t%s_%s.data'%(sim_name,topo.sim.timestr(),
                                                        name.replace(' ','_'))),'wb')
        pickle.dump((topo.version,views),f)
        f.close()
    

def test(plotgroup_names):
    import topo
    import param
    assert topo.sim.name==sim_name
    assert topo.sim['V1'].nominal_density==8
    assert topo.sim.time()==100
    
    for name in plotgroup_names:
        print "\n* Testing plotgroups['%s']:"%name

        sheet = topo.sim['V1']
        _reset_views(sheet)
        plotgroups[name]._exec_pre_plot_hooks()

        f = open(resolve_path('tests/%s_t%s_%s.data'%(sim_name,topo.sim.timestr(),
                                                      name.replace(' ','_'))),'r')

        try:
            topo_version,previous_views = pickle.load(f)
        except AttributeError:
            import topo.misc.legacy
            param.Parameterized().debug("Loading legacy bounding region support.")
            topo.misc.legacy.boundingregion_not_parameterized()
            f.seek(0)
            topo_version,previous_views = pickle.load(f)

        f.close()

        if 'sheet_views' in previous_views[sheet.name]:
            previous_sheet_views = previous_views[sheet.name]['sheet_views']
            for view_name in previous_sheet_views:
                assert_array_almost_equal(sheet.sheet_views[view_name].view()[0],
                                          previous_sheet_views[view_name].view()[0],
                                          12)
                print '...'+view_name+' array is unchanged since data was generated (%s)'%topo_version

        if 'curve_dict' in previous_views[sheet.name]:
            previous_curve_dicts = previous_views[sheet.name]['curve_dict']
            # CB: need to cleanup var names e.g. val
            for curve_name in previous_curve_dicts:
                for other_param in previous_curve_dicts[curve_name]:
                    for val in previous_curve_dicts[curve_name][other_param]:

                        assert_array_almost_equal(sheet.curve_dict[curve_name][other_param][val].view()[0],
                                                  previous_curve_dicts[curve_name][other_param][val].view()[0],
                                                  12)
                        print "...%s %s %s array is unchanged since data was generated (%s)"%(curve_name,other_param,val,topo_version)
                                          


