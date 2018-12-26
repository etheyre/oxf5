import sys, random

from load import *
from util import *

def stopstr(s):
    """ Renvoie : "<nom du stop> (identifiant)" """
    
    return stop_names[s] + " (" + s + ")"

if len(sys.argv) >= 2:
    city = sys.argv[1]
else:
    city = "lyon"

load(city)

if len(sys.argv) != 5:
    print("default parameters")
    dep_stop = stops[random.randint(0, len(stops))]
    arr_stop = stops[random.randint(0, len(stops))]
    dep_time = time2s("07:15:00")
else:
    dep_stop, arr_stop, dep_time = sys.argv[2], sys.argv[3], time2s(sys.argv[4])
        
print(stopstr(dep_stop) + "@" + s2time(dep_time) + " -> " + stopstr(arr_stop) + " (" + city + ")")
print(str(len(stops)) + " stops et " + str(len(connections)) + " connexions")
        
sl = {}

for s in eq_stations:
    sl[s] = None
    if s == parent_stations[dep_stop]:
        sl[s] = Connection(None, None, s, dep_time, ctype = conn_type.BEGIN) # la "connexion" du début (arrivée à la station)

neighbours = {}
        
for s1 in eq_stations:
    neighbours[s1] = []
    for s2 in eq_stations:
        if s1 != s2 and walk_time(geo_stations[s1], geo_stations[s2]) <= 0.2:
            neighbours[s1].append(s2)

begin = 0

transfer_t = 60
        
for k, c in enumerate(connections):
    if dep_time <= c.dept:
        begin = k
        break
        
for c in connections[begin:]:
    deps, dept, arrs, arrt = c.deps, c.dept, c.arrs, c.arrt

    if sl[parent_stations[arr_stop]] != None and dept > sl[parent_stations[arr_stop]].arrt:
        break
    
    if sl[parent_stations[deps]] != None and sl[parent_stations[deps]].arrt + transfer_t <= dept:
        if sl[parent_stations[arrs]] == None:
            sl[parent_stations[arrs]] = c
        elif parent_stations[arrs] != parent_stations[dep_stop] and arrt <= sl[parent_stations[arrs]].arrt:
            # c'est mieux !
            sl[parent_stations[arrs]] = c
            for s in neighbours[parent_stations[arrs]]:
                foot_arrt = c.arrt + walk_time(geo_stations[parent_stations[arrs]], geo_stations[parent_stations[s]])
                conn = Connection(parent_stations[arrs], c.arrt, parent_stations[s], foot_arrt, ctype = conn_type.FOOT)
                if sl[parent_stations[s]] == None:
                    sl[parent_stations[s]] = conn
                elif parent_stations[s] != parent_stations[dep_stop] and foot_arrt <= sl[parent_stations[s]].arrt:
                    sl[parent_stations[s]] = conn
                
s = parent_stations[arr_stop]

route = []

while True:
    c = sl[s]
    route.append(c)
    if c == None:
        print("not reachable")
        exit(-1)
    s = parent_stations[c.deps]
    if s == parent_stations[dep_stop]:
        break

print(bcolor.BOLD, "route", bcolor.END)

beg_stop, beg_time = dep_stop, route[-1].arrt
curr_route = ""
curr_route_name = ""

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

print("total time:", s2time(route[0].arrt - dep_time))
print("transit time:", s2time(route[0].arrt - route[-1].dept))

assert(sl[parent_stations[dep_stop]] == Connection(None, None, parent_stations[dep_stop], dep_time, ctype = conn_type.BEGIN))

for s, c in sl.items():
    if c != None:
        try:
            assert(parent_stations[s] == parent_stations[c.arrs])
        except:
            print(s, c)
        if c.dept != None:
            assert(c.dept <= c.arrt)

"""
maintenant qu'il y a des trajets à pied, il faut enlever l'équivalence station-station parent ; cela permettra peut-être d'éviter trop de correspondances.
"""
