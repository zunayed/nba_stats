from bs4 import BeautifulSoup
import re

fg_data = {}
fg3_data = {}

soup = BeautifulSoup(open('knicks_stats.html'))

all_tr = soup.find_all("tr")

for item in all_tr:
    game_id = item.find_all("td", {'class': "col-Game_ID_SORT"})
    fg_pct = item.find_all("td", {'class': "col-FG_PCT"})
    fg3_pct = item.find_all("td", {'class': "col-FG3_PCT"})

    a = [d.get_text() for d in game_id]
    b = [d.get_text() for d in fg_pct]
    c = [d.get_text() for d in fg3_pct]

    if len(a) > 0:
        team = re.sub('[@, vs , .]', '', a[0][19:])
        fg_data[team] = {
            'fg %': float(b[0].replace("%", "")),
            '3pt %': float(c[0].replace("%", ""))}

for key, value in fg_data.iteritems():
    print key, value
