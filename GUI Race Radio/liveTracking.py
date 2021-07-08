from bs4 import BeautifulSoup as bs
import datetime as dt

def getTracking(liveDict):
    try:
        with open(liveDict["Link"]) as site:
            html = bs(site, "html.parser")
            stats = html.find_all("td")
            info = {stats[i].getText(): stats[i + 1].getText() for i in range(0, len(stats), 2)}
            current_speed = info["Current speed"]
            rm_loc = info["Route mile"]
            distance_2pit = round(pitloc - float(rm_loc.replace(" mi", "")), 2)
    except:
#ADD CODE TO RETURN UPDATED DICT
    return liveDict


