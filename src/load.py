connections = []
stops = []
stop_names = {}
parent_stations = {}
geo_stations = {}
eq_stations = [] # list of parent stations (equivalent stations)

class conn_type:
    VEHICLE = 0
    FOOT = 1
    BEGIN = 2

class Connection:
	def __init__(self, deps, dept, arrs, arrt, trip_id = None, service_id = None, route_id = None, route_name = None, ctype = conn_type.VEHICLE):
		self.deps = deps
		self.dept = dept
		self.arrs = arrs
		self.arrt = arrt
		self.trip_id = trip_id
		self.service_id = service_id
		self.route_id = route_id
		self.route_name = route_name
		self.ctype = ctype

	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__

	def __neq__(self, other):
		return not self == other

def load(city, dept = 0, N = 0):
    with open("data/" + city + "/connections.dat", "r") as f:
        for l in f.readlines():
            ls = l[:-1].split(",")
            if int(ls[1]) >= dept:
	            connections.append(Connection(ls[0], int(ls[1]), ls[2], int(ls[3]), ls[4], ls[5], ls[6], ls[7], conn_type.VEHICLE))

    with open("data/" + city + "/stops.dat", "r") as f:
        for l in f.readlines():
            ls = l.split(",")
            stops.append(ls[0])
            stop_names[ls[0]] = ls[1]
            geo_stations[ls[0]] = (float(ls[2]), float(ls[3]))
            parent_stations[ls[0]] = ls[4][:-1]
            if not ls[4][:-1] in eq_stations:
                eq_stations.append(ls[4][:-1])
