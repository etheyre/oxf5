connections = []
stops = []
stop_names = {}
parent_stations = {}
geo_stations = {}
eq_stations = [] # list of parent stations (equivalent stations)

def load(city):
    with open(city + "/connections.dat", "r") as f:
        for l in f.readlines():
            ls = l[:-1].split(",")
            connections.append((ls[0], int(ls[1]), ls[2], int(ls[3]), ls[4], ls[5], ls[6], ls[7]))

    with open(city + "/stops.dat", "r") as f:
        for l in f.readlines():
            ls = l.split(",")
            stops.append(ls[0])
            stop_names[ls[0]] = ls[1]
            geo_stations[ls[0]] = (float(ls[2]), float(ls[3]))
            parent_stations[ls[0]] = ls[4][:-1]
            if not ls[4][:-1] in eq_stations:
                eq_stations.append(ls[4][:-1])
