"""
Crée un fichier qui contient la table d'horaires de CSA,
et un autre qui contient la liste des arrêts
"""

import sys
from util import *

if len(sys.argv) != 2:
    print("not enough arguments")
    exit(-1)

city = sys.argv[1]

stops = []

with open("data/" + city + "/stops.txt", "r") as f:
    with open("data/" + city + "/stops.dat", "w") as fo:
        beg = f.readline()
        ls = beg[:-1].split(",")
        k = ls.index("stop_lat")
        k2 = ls.index("parent_station")
        for l in f.readlines():
            ls = l.split(",")
            parent_stop = ls[k2].strip()
            stops.append((ls[0], ls[1], float(ls[k].strip()), float(ls[k+1].strip())))
            if parent_stop == "\"\"" or parent_stop == "":
                parent_stop = ls[0]
            fo.write(ls[0] + "," + ls[1] + "," + ls[k].strip() + "," + ls[k+1].strip() + "," + parent_stop + "\n") # stop_id, stop_name, lat, lon, parent_station

with open("data/" + city + "/neighbours.dat", "w") as f:
	for s1 in stops:
		f.write(s1[0] + " ")
		for s2 in stops:
			if s1 != s2 and walk_time((s1[2], s1[3]), (s2[2], s1[3])) <= 10*60:
				f.write(s2[0] + " ")
		f.write("\n")
            
routes = {}

with open("data/" + city + "/routes.txt", "r") as f:
    for l in f.readlines()[1:]:
        ls = l.split(",")
        routes[ls[0]] = ls[2]

trips = {}
        
with open("data/" + city + "/trips.txt", "r") as f:
    for l in f.readlines()[1:]:
        ls = l.split(",")
        trips[ls[2]] = (ls[0], ls[1])

stop_times = {}
n_stop_times = 0

with open("data/" + city + "/stop_times.txt", "r") as f:
    for l in f.readlines()[1:]:
        ls = l.split(",")
        trip_id = ls[0]
        stop_sequence = int(ls[4])
        stop_id = ls[3]
        dep_time = ls[2]
        arr_time = ls[1]
        if not trip_id in stop_times:
            stop_times[trip_id] = [None]*100 # en général, fonctionne
        stop_times[trip_id][stop_sequence] = (stop_id, str(time2s(arr_time)), str(time2s(dep_time)))
        n_stop_times += 1

connections = []

first_deps_ctr = 0

for trip_id, stt in stop_times.items():
    for ss, st in enumerate(stt):
        if ss > 1 and st != None:
            ss_c = ss-1

            while stt[ss_c] == None and ss_c >= 1: # à cause de Metz
                ss_c -= 1

            if ss_c == 0:
                print("WUT")
                exit(-1)    
                
            connections.append((stt[ss_c][0], stt[ss_c][2], st[0], st[1], trip_id, trips[trip_id][1], trips[trip_id][0], routes[trips[trip_id][0]])) # dep_stop, dep_time, arr_stop, arr_time, trip_id, service_id, route_id, route_name
        elif ss <= 1 and st != None:
            first_deps_ctr += 1

print(len(routes), "routes")
print(len(trips), "trips")
print(len(connections), "connections")
print(n_stop_times, "stop_times")
print(first_deps_ctr, "first stops")

assert(n_stop_times == len(connections) + first_deps_ctr)

connections = sorted(connections, key = lambda c: c[1])
            
with open("data/" + city + "/connections.dat", "w") as f:
    for c in connections:
        f.write(",".join(list(c)) + "\n")
