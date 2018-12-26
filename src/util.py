from math import acos, asin, sin, cos, sqrt, pi

class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def isb4(t1, t2):
    h1, m1, s1 = [int(s) for s in t1.split(":")]
    h2, m2, s2 = [int(s) for s in t2.split(":")]
    return h1 < h2 or (h1 == h2 and (m1 < m2 or (m1 == m2 and s1 <= s2)))

def seconds2time(s):
    h = s//3600
    s = s%3600
    m = s//60
    s = s%60
    return str(h) + ":" + str(m) + ":" + str(s)

def timediff(t1, t2):
    """ Renvoie t2 - t1. """

    h1, m1, s1 = [int(s) for s in t1.split(":")]
    h2, m2, s2 = [int(s) for s in t2.split(":")]

    s1 = 3600*h1 + 60*m1 + s1
    s2 = 3600*h2 + 60*m2 + s2

    return seconds2time(s2 - s1)

def normalizetime(t):
    h, m, s = t

    if s >= 60:
        m += s//60
        s %= 60

    if m >= 60:
        h += m//60
        m %= 60

    return (h, m, s)

def h2hms(h):
    h, m, s = normalizetime((0, 0, int(h*3600)))

    return str(h) + ":" + str(m) + ":" + str(s)

def addtime(t1, t2):
    """ Renvoie t1 + t2 """
    h, m, s = [int(x[0]) + int(x[1]) for x in zip(t1.split(":"), t2.split(":"))]

    h, m, s = normalizetime((h, m, s))

    return str(h) + ":" + str(m) + ":" + str(s)
    
def time2s(t):
    """ t: "hh:mm:ss" """

    h, m, s = t.split(":")

    return int(h)*3600 + int(m)*60 + int(s)

def s2time(s):
    m = s//60
    s %= 60
    h = m//60
    m %= 60

    return str(h) + ":" + str(m) + ":" + str(s)

def walk_time(p1, p2):
    """ Renvoie la durée estimée d'une marche à pied entre p1 et p2. """

    # http://edwilliams.org/avform.htm
    lat1, lon1 = p1
    lat2, lon2 = p2
    lat1 *= pi/180
    lat2 *= pi/180
    lon1 *= pi/180
    lon2 *= pi/180
    #d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1-lon2)) * 6371 # rayon de la Terre (km)
    d = 6371 * 2 * asin(sqrt((sin((lat1-lat2)/2))**2 + cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2))**2))
    city_d = sqrt(2)*d # histoires d'escaliers et de diagonales => sqrt(2)*d ?

    walk_speed = 5/3600 # km/s

    return int(city_d/walk_speed) # s
