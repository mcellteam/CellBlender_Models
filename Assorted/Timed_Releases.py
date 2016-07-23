import math

import cellblender as cb
dm = cb.get_data_model()

mcell = dm['mcell']

loops = 3
dt = 1e-6
dc = 5e-5
fr = 200e3

mcell['parameter_system'] = {
    'model_parameters' : [
      { 'par_name' : "loops", 'par_expression' : str(loops) },
      { 'par_name' : "dt", 'par_expression' : str(dt) },
      { 'par_name' : "dc", 'par_expression' : str(dc) },
      { 'par_name' : "fr", 'par_expression' : str(fr) }
    ]
  }

mcell['initialization']['iterations'] = "100"
mcell['initialization']['time_step'] = "dt"


mols = mcell['define_molecules']
mlist = []
nmols = 3
for i in range(nmols):
  new_mol = {
    'custom_space_step' : "",
    'custom_time_step' : "",
    'data_model_version' : "DM_2016_01_13_1930",
    'diffusion_constant' : "dc",
    'display' : {
      'color' : [1.0, 1.0, 1.0],
      'emit' : 2.0,
      'glyph' : "Sphere_1",
      'scale' : 10.0
    },
    'export_viz' : False,
    'maximum_step_length' : "",
    'mol_bngl_label' : "",
    'mol_name' : "m_"+str(i+1),
    'mol_type' : "3D",
    'target_only' : False
  }
  if (i % 3) == 0:
      new_mol['display']['color'] = [1, 0, 0]
  if (i % 3) == 1:
      new_mol['display']['color'] = [1, 1, 1]
  if (i % 3) == 2:
      new_mol['display']['color'] = [0, 0.2, 1]
  mlist.append ( new_mol )

mols['molecule_list'] = mlist

sites = { 'data_model_version' : "DM_2014_10_24_1638" }
slist = []
patterns = { 'data_model_version' : "DM_2014_10_24_1638" }
plist = []
reactions = { 'data_model_version' : "DM_2014_10_24_1638" }
rlist = []

m = 1
n = 2
delta = math.pi / 32

i = 0
path = 0.0
radius = 3.0

while path < (loops * 2 * math.pi) + delta:

  x = radius * math.sin(path*m)
  y = radius * math.sin(path*n)

  p = {
        'data_model_version' : "DM_2014_10_24_1638",
        'delay' : "%d * dt" % i,
        'name' : "t%d" % (i+1),
        'number_of_trains' : "1",
        'release_interval' : "",
        'train_duration' : "",
        'train_interval' : ""
      }
  plist.append ( p )

  s = {
        'data_model_version' : "DM_2015_11_11_1717",
        'location_x' : str(x),
        'location_y' : str(y),
        'location_z' : "0",
        'molecule' : "m_%d" % ((i%nmols)+1),
        'name' : "r_%d" % (i+1),
        'object_expr' : "",
        'orient' : "'",
        'pattern' : "t%d" % (i+1),
        'points_list' : [ [0.0, 0.0, 0.0] ],
        'quantity' : "30",
        'quantity_type' : "NUMBER_TO_RELEASE",
        'release_probability' : "1",
        'shape' : "SPHERICAL",
        'site_diameter' : "0.1",
        'stddev' : "0"
      }
  slist.append ( s )

  if i < nmols:
      r = {
            'bkwd_rate' : "",
            'data_model_version' : "DM_2014_10_24_1638",
            'fwd_rate' : "fr",
            'name' : "r_%d -> NULL" % (i+1),
            'products' : "NULL",
            'reactants' : "m_%d" % ((i%nmols)+1),
            'rxn_name' : "",
            'rxn_type' : "irreversible",
            'variable_rate' : "",
            'variable_rate_switch' : False,
            'variable_rate_text' : "",
            'variable_rate_valid' : False
          }
      rlist.append ( r )
  i += 1
  path += delta

mcell['initialization']['iterations'] = str(i)

patterns['release_pattern_list'] = plist
mcell['define_release_patterns'] = patterns
sites['release_site_list'] = slist
mcell['release_sites'] = sites
reactions['reaction_list'] = rlist
mcell['define_reactions'] = reactions

mcell['geometrical_objects'] = { 'object_list' : [] }
mcell['model_objects'] = { 'data_model_version' : "DM_2014_10_24_1638", 'model_object_list' : [] }


cb.replace_data_model ( dm, geometry=True )
