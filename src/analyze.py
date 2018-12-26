from load import *
from util import *
import kml
import matplotlib.pyplot as plt
import numpy as np

load("lyon2")

def analyze_neighbours(Rd):
    neighbours = {}

    for s1 in eq_stations:
        for s2 in eq_stations:
            if s1 != s2 and walk_time(geo_stations[s1], geo_stations[s2]) <= Rd:
                if s1 not in neighbours:
                    neighbours[s1] = []
                neighbours[s1].append(s2)

    mean = 0
    M = 0
    Ms = ""
    m = len(eq_stations)
    ms = ""
    for k, s in neighbours.items():
        if len(s) > M:
            M = len(s)
            Ms = k
        if len(s) < m:
            m = len(s)
            ms = k
        mean += len(s)

    mean = mean/len(neighbours) # moyenne du nombre de voisins par station
    
    return (mean, (Ms, M), (ms, m))

def sweep_neighbours():
    means = []
    for k in range(0, 10):
        means.append(analyze_neighbours((k+1)/10)[0])
    plt.plot([(k+1)/10 for k in range(0, 10)], means)
    plt.savefig("mean_neighbours.png")
    return means

def conn_density():
    n = 200

    minN, maxN = 90, 0
    minE, maxE = 90, 0
    
    conn_per_station = {}
    
    for c in connections:
        if parent_stations[c[0]] not in conn_per_station:
            conn_per_station[parent_stations[c[0]]] = 0
        if parent_stations[c[2]] not in conn_per_station:
            conn_per_station[parent_stations[c[2]]] = 0
        conn_per_station[parent_stations[c[0]]] += 1
        conn_per_station[parent_stations[c[2]]] += 1

    for s in eq_stations:
        lat, lon = geo_stations[s]
        minN = min(lat, minN)
        maxN = max(lat, maxN)
        minE = min(lon, minE)
        maxE = max(lon, maxE)

    mat = np.zeros((n, n))
    lat_size = 1.0001*(maxN - minN)/n
    lon_size = 1.0001*(maxE - minE)/n
    print(maxN, minN, maxE, minE)

    for s, nc in conn_per_station.items():
        lat, lon = geo_stations[s]
        mat[int((lat-minN)/lat_size)][int((lon-minE)/lon_size)] += nc
    mat = np.sqrt(mat) # pour faire joli
    plt.imshow(mat, cmap = "hot", interpolation = "nearest")
    plt.savefig("density.png")

def stop_density():
    n = 200

    minN, maxN = 90, 0
    minE, maxE = 90, 0

    for s in stops: #eq_stations:
        lat, lon = geo_stations[s]
        minN = min(lat, minN)
        maxN = max(lat, maxN)
        minE = min(lon, minE)
        maxE = max(lon, maxE)

    mat = np.zeros((n, n))
    lat_size = 1.0001*(maxN - minN)/n
    lon_size = 1.0001*(maxE - minE)/n
    print(maxN, minN, maxE, minE)

    for s in stops:
        lat, lon = geo_stations[s]
        mat[int((lat-minN)/lat_size)][int((lon-minE)/lon_size)] += 1
    # mat = np.sqrt(mat) # pour faire joli
    plt.imshow(mat, cmap = "hot", interpolation = "nearest")
    plt.savefig("stop_density.png")