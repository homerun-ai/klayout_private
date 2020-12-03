
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Draw legs and PDL outline for 1 unit mesh (1 display pixel sized)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import pya

layout = pya.Layout()


# Create Cell obj
UNIT = layout.create_cell("0_UNIT")


# Create layer #'s
import layer_numbers as lm
l_1x1_outline = layout.layer(lm.layer_num_1x1_outline, 0) # 1x1 Outline
l_PDL_outline = layout.layer(lm.layer_num_PDL_outline, 0) # PDL Outline
l_metal = layout.layer(lm.layer_num_metal, 0) # Metal


import dimensions as dim
# Mesh dimensions
line_width = dim.line_width
pitch = dim.pitch
h_pitch_RG = dim.h_pitch_RG
h_pitch_B = dim.h_pitch_B
v_pitch_R = dim.v_pitch_R
v_pitch_G = dim.v_pitch_G
v_pitch_B = dim.v_pitch_B


# PDL - R&G
w_pdl_RG = dim.w_pdl_RG
h_pdl_R = dim.h_pdl_R
h_pdl_G = dim.h_pdl_G


# PDL - B
w_pdl_B = dim.w_pdl_B
h_pdl_B = dim.h_pdl_B


print("pitch check --> this # should be == pitch : ", h_pitch_RG + h_pitch_B )


# Draw outline
leg0 = UNIT.shapes(l_1x1_outline).insert( pya.Box(0, 0, pitch, pitch) ) 


# Draw metal legs
leg1 = UNIT.shapes(l_metal).insert( pya.Box(0, 0, line_width, pitch) ) 
leg2 = UNIT.shapes(l_metal).insert( pya.Box(0, pitch-line_width, pitch, pitch) ) 
leg3 = UNIT.shapes(l_metal).insert( pya.Box(0, v_pitch_G-line_width, h_pitch_RG, v_pitch_G) ) 
leg4 = UNIT.shapes(l_metal).insert( pya.Box(h_pitch_RG, 0, h_pitch_RG+line_width, pitch) ) 


# Draw PDL outlines
pdl_g = UNIT.shapes(l_PDL_outline).insert( pya.Box( line_width+(h_pitch_RG-line_width-w_pdl_RG)/2, (v_pitch_G-line_width-h_pdl_G)/2, line_width+(h_pitch_RG-line_width-w_pdl_RG)/2+w_pdl_RG, (v_pitch_G-line_width-h_pdl_G)/2+h_pdl_G) ) 
pdl_r = UNIT.shapes(l_PDL_outline).insert( pya.Box( line_width+(h_pitch_RG-line_width-w_pdl_RG)/2, v_pitch_G+(v_pitch_R-line_width-h_pdl_R)/2, line_width+(h_pitch_RG-line_width-w_pdl_RG)/2+w_pdl_RG, v_pitch_G+(v_pitch_R-line_width-h_pdl_R)/2+h_pdl_R) ) 
pdl_b = UNIT.shapes(l_PDL_outline).insert( pya.Box( h_pitch_RG+line_width+(h_pitch_B-line_width-w_pdl_B)/2, (v_pitch_B-line_width-h_pdl_B)/2, h_pitch_RG+line_width+(h_pitch_B-line_width-w_pdl_B)/2+w_pdl_B, (v_pitch_B-line_width-h_pdl_B)/2+h_pdl_B) ) 


# Export GDS
layout.write("0_unit_dpix_1x1.gds")
