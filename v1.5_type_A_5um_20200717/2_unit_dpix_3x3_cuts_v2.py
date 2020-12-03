
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Import list names for cuts
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


import cell_names as p
cut_d = {
  "unit_2_1" : p.unit_2_1,
  "unit_2_7" : p.unit_2_7,
  "unit_2_14" : p.unit_2_14,
  "unit_3_2" : p.unit_3_2,
  "unit_3_3" : p.unit_3_3,
  "unit_3_4" : p.unit_3_4,
  "unit_3_6" : p.unit_3_6,
  "unit_3_9" : p.unit_3_9,
  "unit_3_12" : p.unit_3_12,
  #"unit_cuts_everywhere" : p.unit_cuts_everywhere,
  "unit_2_4" : p.unit_2_4,
  "unit_14_4" : p.unit_14_4,
  "unit_7_7" : p.unit_7_7,
  "unit_1_7" : p.unit_1_7,
  "unit_1_4" : p.unit_1_4,
  "unit_7_8" : p.unit_7_8,
  "unit_14_6" : p.unit_14_6,
  "unit_14_9" : p.unit_14_9,
  "unit_14_1" : p.unit_14_1,
  "unit_14_2" : p.unit_14_2,
  "unit_14_3" : p.unit_14_3,
  "unit_14_12" : p.unit_14_12,
  "unit_14_14" : p.unit_14_14,
  "unit_7_6" : p.unit_7_6,
  "unit_7_9" : p.unit_7_9,
  "unit_1_1" : p.unit_1_1,
  "unit_1_2" : p.unit_1_2,
  "unit_1_3" : p.unit_1_3,
  "unit_2_2" : p.unit_2_2,
  "unit_2_3" : p.unit_2_3,
  "unit_2_12" : p.unit_2_12,
  "unit_1_12" : p.unit_1_12,
  "unit_1_13" : p.unit_1_13,
  "unit_1_14" : p.unit_1_14,
  "unit_2_6" : p.unit_2_6,
  "unit_2_9" : p.unit_2_9,
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import os
root = os.path.dirname( os.path.abspath(__file__) )


import pya
layout = pya.Layout()
#layout.dbu = 0.001


# Create Cell obj
UNIT = layout.create_cell("1_UNIT_CUTS")


# Define layer #'s
import layer_numbers as lm
l_metal = layout.layer(lm.layer_num_metal, 0) # Metal
l_cut_box = layout.layer(lm.layer_num_cut_box, 0) # Metal



# Define array of GDS to read
gdsFiles=[ "1_unit_dpix_3x3.gds" ]


import dimensions as dim
# Mesh dimensions (as dictionary, so that we can pass on to function)
d = {
  "line_width": dim.line_width,
  "cut_width": dim.cut_width,
  "pitch": dim.pitch,
  "h_pitch_RG": dim.h_pitch_RG,
  "h_pitch_B": dim.h_pitch_B,
  "v_pitch_R": dim.v_pitch_R,
  "v_pitch_G": dim.v_pitch_G,
  "v_pitch_B": dim.v_pitch_B
}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

 
def main():
  # Loop each cut map, & export each GDS as unique name
  for key in cut_d:
    filename = "2_" + key # Add prefix to the filename
    print ( "\nfilename : ", filename )
  
    # Get 1_UNIT (no cuts as a reference) & create SINGLE instance
    for i in gdsFiles:
      layout.read(i)

      for cell in layout.top_cells():
        # we don't want to insert the topcell itself
        if (cell.name != "1_UNIT_CUTS"):
          print ( "Adding : " + cell.name )
          cell_index=cell.cell_index()
          new_instance=pya.CellInstArray( cell_index, pya.Trans(pya.Point(0,0)) )
          UNIT.insert( new_instance )


    # Define imported metal as a region (for boolean)
    region_metal = pya.Region( layout.top_cell().begin_shapes_rec(l_metal) )


    # Define cut area & make as region
    for ind, each_cut in enumerate(cut_d[key]):
      cut_box_coord = get_cut_coord( each_cut, d )
      UNIT.shapes(l_cut_box).insert( cut_box_coord ) 
      region_cut_box = pya.Region( cut_box_coord )   
      # Do boolean (XOR)
      # For more than 1 cuts, need to loop and take XOR of previous XOR results
      if ind == 0:
        region_xor = region_metal ^ region_cut_box
      else:
        region_xor = region_xor ^ region_cut_box


    # Remove existings metal layer + cut boxes
    # (!!! SKIP THIS TO CHECK CUT BOXES IN GDS !!!)
    layout.clear_layer(l_metal)
    layout.clear_layer(l_cut_box)


    # INSERT BOOLEAN RESULT AS ORIGINAL METAL LAYER
    UNIT.shapes(l_metal).insert(region_xor)


    # Check if filename gds exists -> If so skip "write"
    if os.path.isfile( root+"/"+filename+".gds" ):
      print ("**** GDS name by : "+filename+".gds already exists!" )
      print ("**** SKIPPING GDS WRITE!!!" )
    else:
      # Export GDS
      layout.write( filename+".gds" )

      # Check if this cell can be used as another at different coordinate
      dup_l = get_dup_names( filename+".gds" )
      if dup_l[0] != '':
        for each in dup_l:
          print("Create copy as : ", each, "  <-----------------------------------------")
          layout.write( each )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


def get_dup_names( filename ):
  if filename == '2_unit_2_7.gds':
    return [ '2_unit_8_7.gds', '2_unit_14_7.gds' ]
  
  elif filename == '2_unit_3_4.gds':
    return [ '2_unit_3_10.gds', '2_unit_2_13.gds', '2_unit_3_13.gds', '2_unit_14_13.gds' ]
    
  elif filename == '2_unit_3_6.gds':
    return [ '2_unit_8_6.gds' ] 

  elif filename == '2_unit_3_9.gds':
    return [ '2_unit_8_9.gds' ] 

  elif filename == '2_unit_14_4.gds':
    return [ '2_unit_14_10.gds' ]

  elif filename == '2_unit_1_4.gds':
    return [ '2_unit_1_9.gds' ] 

  elif filename == '2_unit_2_4.gds':
    return [ '2_unit_2_10.gds' ]  

  else:
    return [ '' ]


def get_cut_coord( each_cut_s, d ):
  # First, get COL number from name ("2g_l")
  if "1" in each_cut_s or "4" in each_cut_s or "7" in each_cut_s:
    col = 0
  elif "2" in each_cut_s or "5" in each_cut_s or "8" in each_cut_s:
    col = 1
  elif "3" in each_cut_s or "6" in each_cut_s or "9" in each_cut_s:
    col = 2
 
  # Next, get ROW number from name ("2g_l")
  if "1" in each_cut_s or "2" in each_cut_s or "3" in each_cut_s:
    row = 0
  elif "4" in each_cut_s or "5" in each_cut_s or "6" in each_cut_s:
    row = 1
  elif "7" in each_cut_s or "8" in each_cut_s or "9" in each_cut_s:
    row = 2
      
  # Get location info from name ("2g_l")
  # (pre-define some of re-used coordinates here)
  g_l_x1 = d["pitch"]*col
  g_l_x2 = d["pitch"]*col+d["line_width"]
  g_l_y1 = d["pitch"]*row+(d["v_pitch_G"]-d["line_width"])/2-d["cut_width"]/2
  g_l_y2 = d["pitch"]*row+(d["v_pitch_G"]-d["line_width"])/2+d["cut_width"]/2
  g_r_x1 = d["pitch"]*col+d["h_pitch_RG"]
  g_r_x2 = d["pitch"]*col+ d["h_pitch_RG"]+d["line_width"]
  r_l_y1 = d["pitch"]*row+d["v_pitch_G"]+(d["v_pitch_R"]-d["line_width"])/2-d["cut_width"]/2
  r_l_y2 = d["pitch"]*row+d["v_pitch_G"]+(d["v_pitch_R"]-d["line_width"])/2+d["cut_width"]/2
  r_t_x1 = d["pitch"]*col+d["line_width"]+(d["h_pitch_RG"]-d["line_width"])/2-d["cut_width"]/2
  r_t_x2 = d["pitch"]*col+d["line_width"]+(d["h_pitch_RG"]-d["line_width"])/2+d["cut_width"]/2
  r_t_y1 = d["pitch"]*row+(d["pitch"]-d["line_width"])
  r_t_y2 = d["pitch"]*row+d["pitch"]
  
  if "g_l" in each_cut_s:
    cut_box = pya.Box( d["pitch"]*col, g_l_y1, d["pitch"]*col+d["line_width"], g_l_y2 )
  elif "g_r" in each_cut_s:
    cut_box = pya.Box( d["pitch"]*col+d["h_pitch_RG"], g_l_y1, d["pitch"]*col+ d["h_pitch_RG"]+d["line_width"], g_l_y2 )
  elif "r_l" in each_cut_s:
    cut_box = pya.Box( g_l_x1, r_l_y1, g_l_x2, r_l_y2 )  
  elif "r_r" in each_cut_s:
    cut_box = pya.Box( g_r_x1, r_l_y1, g_r_x2, r_l_y2 ) 
  elif "r_t" in each_cut_s:
    cut_box = pya.Box( r_t_x1, r_t_y1, r_t_x2, r_t_y2 ) 
  elif "r_b" in each_cut_s:
    cut_box = pya.Box( 
      r_t_x1, 
      d["pitch"]*row+(d["v_pitch_G"]-d["line_width"]), 
      r_t_x2, 
      d["pitch"]*row+d["v_pitch_G"] ) 
  elif "b_t" in each_cut_s:
    cut_box = pya.Box( 
      d["pitch"]*col+d["h_pitch_RG"]+d["line_width"]+(d["h_pitch_B"]-d["line_width"])/2-d["cut_width"]/2, 
      r_t_y1, 
      d["pitch"]*col+d["h_pitch_RG"]+d["line_width"]+(d["h_pitch_B"]-d["line_width"])/2+d["cut_width"]/2, 
      r_t_y2 ) 
  else:
    print ("NO cut name such as : ", each_cut_s )
  return cut_box


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


if __name__ == '__main__':
  main()