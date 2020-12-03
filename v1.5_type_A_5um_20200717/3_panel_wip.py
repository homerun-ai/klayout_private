 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# From all GDS, only read the ones that start with "2_..." (e.g. 2_unit_1_7.gds)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Ignore 1st char, and get (x,y) coordinates from remaining part of the filename
# Save as dict
# Key : gds filename (str), Value : xy coord (list)
import glob

gds_files_d = {}
for ind, each_file in enumerate ( glob.glob ( "*.gds") ):
  if each_file[0] == "2":
    print ( "\nEach GDS that starts with 2_unit_...: ", each_file )
    temp_str = each_file[1:].replace('_', ' ').replace('.', ' ')
    # print ( "temp_str : ", temp_str )
    xy_l = [ int(s) for s in temp_str.split() if s.isdigit() ]
    print ( "(X,Y) Coordinates (in 3x3 pitches) : ", xy_l )
    gds_files_d[ each_file ] = xy_l
# print ( "\ngds_files_d : ", gds_files_d )

"""
gds_files_d :  {
  '2_unit_1_7.gds': [1, 7], 
  '2_unit_7_7.gds': [7, 7], 
  ... 
}
"""


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# BELOW FLOW IS BASED ON "reading_two_gds_into_one.py"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import dimensions as dim
# Pitch of cells (to be placed as instances)
p = dim.pitch*3 # 96 x 3 = 288um


def main():
  # [1] Create TOP layout (LAYOUT_TOP, where layouts A,B,... would be merged)
  import pya
  LAYOUT_TOP = pya.Layout()
  CELL_TOP = LAYOUT_TOP.create_cell("CELL_TOP")
  # Create layer #'s
  import layer_numbers as lm
  l_TP_outline = LAYOUT_TOP.layer(lm.layer_num_TP_outline, 0) # One touch pixel Outline
  # Insert box outline for unit touch pixel dimensions
  CELL_TOP.shapes(l_TP_outline).insert( pya.Box(0, 0, p*14, p*14) ) 


  for ind, (k, v) in enumerate ( gds_files_d.items() ):
    print ( "\nProcessing ... : ", ind, k, v ) # 0 | 2_unit_1_7.gds | [1, 7]
    # [2] Loop over each GDS, create separate layouts (LAYOUT_A, LAYOUT_B, ...), and read each GDS files
    LAYOUT_A = pya.Layout()
    LAYOUT_A.read( k )

    # From GDS name, get # of repeats in x-y dir
    [nx, ny] = get_nx_ny(k)
    #[nx, ny] = [1, 1]
    
    # [3] In TOP layout, create (empty) target cells (ta, tb, ...) 
    CELL_TA = LAYOUT_TOP.create_cell( "CELL_" + str(v[0]) + "_" + str(v[1]) ) # CELL_2_7, CELL_14_5, ...
    CELL_TOP.insert( 
      pya.CellInstArray( 
        CELL_TA.cell_index(), 
        pya.Trans(pya.Point( p*(v[1]-1), p*(v[0]-1) )),
        pya.Vector(p, 0), 
        pya.Vector(0, p), 
        nx, ny  
      ) 
    )
      # v : value (e.g. [1, 7]) --> x = v[1], y = v[0]

    # [4] From [3], copy over the layouts from A to TA, using ta.move_tree(layout_A.top_cell() )
    CELL_TA.move_tree( LAYOUT_A.top_cell() )


  # Export GDS
  LAYOUT_TOP.write( "3_PANEL_wip.gds" )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_nx_ny(filename):
  if filename == '2_unit_2_1.gds' or filename == '2_unit_2_14.gds':
    return [1, 12]
  elif filename == '2_unit_2_7.gds':
    return [2, 5]
  elif filename == '2_unit_8_7.gds':
    return [2, 6]
  elif (filename == '2_unit_14_7.gds' or filename == '2_unit_14_4.gds' or 
    filename == '2_unit_14_10.gds' or filename == '2_unit_1_7.gds' or 
    filename == '2_unit_2_4.gds' or filename == '2_unit_2_10.gds'):
    return [2, 1]
  elif filename == '2_unit_3_12.gds' or filename == '2_unit_3_2.gds' or filename == '2_unit_3_13.gds':
    return [1, 11]
  elif filename == '2_unit_3_3.gds':
    return [1, 11]
  elif filename == '2_unit_3_4.gds':
    return [2, 11]
  elif filename == '2_unit_3_10.gds':
    return [2, 11]
  elif filename == '2_unit_3_6.gds' or filename == '2_unit_3_9.gds':
    return [1, 4]
  elif filename == '2_unit_8_6.gds' or filename == '2_unit_8_9.gds':
    return [1, 6]
  elif filename == '2_unit_1_4.gds' or filename == '2_unit_1_9.gds':
    return [3, 1]
  else:
    return [1, 1]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == '__main__':
  main()