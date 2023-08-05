# demonstrate how to convert MGRS to GPS coordinates 
#  in degrees, minutes, seconds

import math
from ctypes import *
from jaraco.geo.geotrans import *
from jaraco.geo.geotrans2_lib import *
from jaraco.geo import DMS

PI = math.pi

def test_convert():
	datum_index = c_long()

	ce90 = c_double(1.0)
	le90 = c_double(1.0)
	se90 = c_double(1.0)

	input_coords = MGRS_Tuple()
	input_coords.string = '38SLC6902909968' # somewhere in iraq

	output_params = Geodetic_Parameters()
	output_params.height_type = Ellipsoid_Height
	output_coords = Geodetic_Tuple()

	handle_status(Initialize_Engine())
	handle_status(Get_Datum_Index ("WGE", datum_index))
	handle_status(Set_Datum (Interactive, Input, datum_index))
	handle_status(Set_Coordinate_System (Interactive, Input, MGRS))
	#handle_status(Set_MGRS_Params (Interactive, Input, input_params))
	handle_status(Set_MGRS_Coordinates (Interactive, Input, input_coords))
	handle_status(Set_Datum (Interactive, Output, datum_index))
	handle_status(Set_Coordinate_System (Interactive, Output, Geodetic))
	handle_status(Set_Geodetic_Params (Interactive, Output, output_params))
	handle_status(Convert(Interactive))
	handle_status(Get_Geodetic_Coordinates (Interactive, Output, output_coords))
	#handle_status(Get_Conversion_Errors (Interactive, ce90, le90, se90)) 

	print "latitude:", unicode(DMS(output_coords.latitude*180/PI))
	print "longitude:", unicode(DMS(output_coords.longitude*180/PI))

if __name__ == '__main__': test_convert()
