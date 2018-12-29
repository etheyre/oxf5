import sys, random, time

from load import *
from util import *

def stopstr(s):
    """ Renvoie : "<nom du stop> (identifiant)" """
    
    return stop_names[s] + " (" + s + ")"

if len(sys.argv) != 5:
    print("default parameters")
    dep_stop = stops[random.randint(0, len(stops))]
    arr_stop = stops[random.randint(0, len(stops))]
    dep_time = time2s("07:15:00")
else:
    dep_stop, arr_stop, dep_time = sys.argv[2], sys.argv[3], time2s(sys.argv[4])

if len(sys.argv) >= 2:
    city = sys.argv[1]
else:
    city = "lyon"

start_time = time.time()
load(city, dept = dep_time)
print("loading time:", time.time() - start_time)
        
print(stopstr(dep_stop) + "@" + s2time(dep_time) + " -> " + stopstr(arr_stop) + " (" + city + ")")
print(str(len(stops)) + " arrêts et " + str(len(connections)) + " connexions")

sl = {}

for s in stops:
    sl[s] = None
	
sl[dep_stop] = Connection(None, None, dep_stop, dep_time, ctype = conn_type.BEGIN) # la "connexion" du début (arrivée à la station)

neighbours = {}

start_time = time.time()

with open("data/" + city + "/neighbours.dat", "r") as f:
	for l in f.readlines():
		ls = l.split(" ")
		if len(ls) < 2:
			print("incorrect neighbours.dat file")
			exit(-1)
		neighbours[ls[0]] = ls[1:-1]

print("neighbours building time:", time.time() - start_time)
			
start_time = time.time()

foot_updates = [dep_stop]

begin = 0

transfer_t = 60*3
		
for k, c in enumerate(connections): # remplacer ça par une dichotomie
	if dep_time <= c.dept:
		begin = k
		break

n_updates = 0
n_connections = 0
n_foot_updates = 0

for c in connections[begin:]:
	deps, dept, arrs, arrt = c.deps, c.dept, c.arrs, c.arrt

	if sl[arr_stop] != None and dept > sl[arr_stop].arrt:
		break

	n_connections += 1
	
	if sl[deps] != None \
	   and ((c.trip_id == sl[deps].trip_id and sl[deps].arrt <= dept) \
			or sl[deps].arrt + transfer_t <= dept):
		if sl[arrs] == None:
			sl[arrs] = c
			foot_updates.append(arrs)
		elif arrt <= sl[arrs].arrt: # si c'est égal, priviliégier celui qui ne fait pas changer de mode de transport ?
			# c'est mieux !
			sl[arrs] = c
			foot_updates.append(arrs)
			n_updates += 1

	while(len(foot_updates) != 0):
		beg_s = foot_updates.pop()
		for s in neighbours[beg_s]:
			foot_arrt = sl[beg_s].arrt + walk_time(geo_stations[beg_s], geo_stations[s])
			conn = Connection(beg_s, sl[beg_s].arrt, s, foot_arrt, ctype = conn_type.FOOT)
			if sl[s] == None:
				sl[s] = conn
				foot_updates.append(s)
			elif sl[s] != None and foot_arrt < sl[s].arrt:
				sl[s] = conn
				n_updates += 1
				n_foot_updates += 1

s = arr_stop

route = []

while True:
	c = sl[s]
	route.append(c)
	if c == None:
		print("not reachable")
		exit(-1)
	s = c.deps
	if s == dep_stop:
		break

end_time = time.time()

print("number of updates:", n_updates)
print("number of foot updates:", n_foot_updates)
print("number of connections:", str(n_connections) + "/" + str(len(connections)))
					
n_reached = 0

for s, v in sl.items():
	if v != None:
		n_reached += 1

print("number of reached stations:", str(n_reached) + "/" + str(len(stops)))

print(bcolor.BOLD, "route", bcolor.END)

beg_stop, beg_time = dep_stop, route[-1].arrt
curr_route = ""
curr_route_name = ""

devel_out = True

if not devel_out:
	for c in reversed(route):
		deps, dept, arrs, arrt, route_id, route_name, ctype = c.deps, c.dept, c.arrs, c.arrt, c.route_id, c.route_name, c.ctype

		route_or_type = route_id
		if ctype == conn_type.FOOT:
			route_or_type = ctype

		if curr_route != route_or_type and curr_route != "":
			if curr_route == conn_type.FOOT:
				print(bcolor.BOLD, "à pied", bcolor.END)
			else:
				print(bcolor.BOLD, "route:", curr_route, "(", curr_route_name, ")", bcolor.END)
			print("\t" + stopstr(beg_stop), "@", s2time(beg_time), "->", stopstr(arrs), "@", s2time(dept))
			beg_stop = arrs
			beg_time = arrt
			curr_route = route_or_type
			curr_route_name = route_name
		elif curr_route == "":
			curr_route = route_or_type
			curr_route_name = route_name
else:
	for i, c in enumerate(reversed(route)):
		deps, dept, arrs, arrt, trip_id, route_id, route_name, service_id, ctype = c.deps, c.dept, c.arrs, c.arrt, c.trip_id, c.route_id, c.route_name, c.service_id, c.ctype
		if i % 2 == 0:
			print(bcolor.OKBLUE, end="")
		
		print(stopstr(deps).ljust(50, " ") + s2time(dept).ljust(10, " ") + stopstr(arrs).ljust(50, " ") + s2time(arrt).ljust(10, " "), end="")
		
		if ctype == conn_type.FOOT:
			print("à pied")
		else:
			print(route_name.ljust(7, " ") + route_id.ljust(10, " ") + trip_id.ljust(25, " ") + service_id.ljust(25, " "))

		if i % 2 == 0:
			print(bcolor.END, end="")

print("total time:", s2time(route[0].arrt - dep_time))
print("transit time:", s2time(route[0].arrt - route[-1].dept))
print("processing time:", end_time - start_time)

assert(sl[dep_stop] == Connection(None, None, dep_stop, dep_time, ctype = conn_type.BEGIN))

for s, c in sl.items():
	if c != None:
		try:
			assert(s == c.arrs)
		except:
			print(s, c)
		if c.dept != None:
			assert(c.dept <= c.arrt)
