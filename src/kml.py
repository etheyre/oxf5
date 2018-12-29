def write(coords, filename):
	with open("res/" + filename, "w") as f:
		f.write("""<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n""")
		for c in coords:
			station, cc = c
			lon, lat = cc
			f.write("<Placemark>\n<name>" + station + "</name>\n<Point>\n<coordinates>" + str(lat) + "," + str(lon) + "</coordinates>\n</Point>\n</Placemark>\n")
		f.write("</Document></kml>")


def plot_all_stations():
	write([(s, geo_stations[s]) for s in eq_stations], "all_stations.kml")
