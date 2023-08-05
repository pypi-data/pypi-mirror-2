from jaraco.geo.geotrans import initialize_engine, get_datum_index

def test_get_index():
	initialize_engine()
	print get_datum_index('WGE')

if __name__ == '__main__': test_get_index()
