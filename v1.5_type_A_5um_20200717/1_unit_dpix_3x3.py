
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Based on 1 unit mesh (1 display pixel sized), create 3x3 unit mesh
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import pya

layout = pya.Layout()
#layout.dbu = 0.001


# Create Cell obj
UNIT = layout.create_cell("1_UNIT")


# Create layer #'s
import layer_numbers as lm
l_3x3_outline = layout.layer(lm.layer_num_3x3_outline, 0) # 3x3 Outline


# Define array of GDS to read
gdsFiles=[ "0_unit_dpix_1x1.gds" ]


import dimensions as dim
# Mesh dimensions
pitch = dim.pitch


# Get 0_UNIT & create 3x3 instance
for i in gdsFiles:
  layout.read(i)

  for cell in layout.top_cells():
    # we don't want to insert the topcell itself
    if (cell.name != "1_UNIT"):
    	print ( "Adding " + cell.name )
    	cell_index=cell.cell_index()
    	new_instance=pya.CellInstArray( cell_index, pya.Trans(pya.Point(0,0)), pya.Vector(pitch, 0), pya.Vector(0, pitch), 3, 3 )
    		# pya.Trans(pya.Point(0,0)) --> defines the LOCATION at which instanace should be placed
    		# pya.Vector(pitch, 0) --> defines the PITCH at which instance should repeat
    		# 3, 3 --> defines number of repeats
    	UNIT.insert( new_instance )


# Draw outline (of 3x3)
UNIT.shapes(l_3x3_outline).insert( pya.Box(0, 0, 3*pitch, 3*pitch) ) 


# Export GDS
layout.write("1_unit_dpix_3x3.gds")