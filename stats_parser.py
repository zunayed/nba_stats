'''
http://stats.nba.com/
teamGameLogs.html?TeamID=1610612752&pageNo=1&rowsPerPage=100
'''

from bs4 import BeautifulSoup
import re
import io
import json


def parse_html_data(location):
    soup = BeautifulSoup(open(location))
    data = {}
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

            if team in data:
                data[team]['fg %'].append(float(b[0].replace("%", "")))
                data[team]['3pt %'].append(float(c[0].replace("%", "")))
            else:
                data[team] = {
                    'fg %': [float(b[0].replace("%", ""))],
                    '3pt %': [float(c[0].replace("%", ""))]
                }

    return data


def convert_teams_to_states(data):
    nba_teams = {
        'MIL': 'Wisconsin',
        'MIN': 'Minnesota',
        'MIA': 'Miami',
        'ATL': 'Georgia',
        'BOS': 'Massachusetts',
        'DET': 'Michigan',
        'DEN': 'Colorado',
        'SAC': 'California',
        'BKN': 'New York',
        'POR': 'Oregon',
        'ORL': 'Florida',
        'TOR': 'Canada',
        'CHI': 'Illinois',
        'SAS': 'Texas',
        'CHA': 'North Carolina',
        'CLE': 'Ohio',
        'WAS': 'Maryland',
        'LAL': 'California',
        'PHI': 'Pennsylvania',
        'MEM': 'Tennessee',
        'LAC': 'California',
        'DAL': 'Texas',
        'OKC': 'Oklahoma',
        'PHX': 'Arizona',
        'IND': 'Indiana',
        'NOP': 'Louisiana',
        'HOU': 'Texas'
    }

    new_data = {}

    for team, value in data.iteritems():
        # if team in same state combine %s
        if nba_teams[team] in new_data:
            new_data[nba_teams[team]]['fg %'] = new_data[
                nba_teams[team]]['fg %'] + value['fg %']
            new_data[nba_teams[team]]['3pt %'] = new_data[
                nba_teams[team]]['3pt %'] + value['3pt %']
        else:
            new_data[nba_teams[team]] = value

    return new_data


def sum_avg(data):
    for key, value in data.iteritems():
        fg_avg = sum(value['fg %']) / len(value['fg %'])
        three_avg = sum(value['3pt %']) / len(value['3pt %'])

        data[key]['fg %'] = fg_avg
        data[key]['3pt %'] = three_avg

    return data


def output_to_json(data):
    with io.open('data.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))


data = sum_avg(convert_teams_to_states(parse_html_data('knicks_stats.html')))

for key, value in data.iteritems():
    print key, value

output_to_json(data)

nba_team_ids = {
    'Atlanta Hawks': 1610612737,
    'Boston Celtics': 1610612738,
    'Brooklyn Nets': 1610612751,
    'Charlotte Hornets': 1610612766,
    'Chicago Bulls': 1610612741,
    'Cleveland Cavaliers': 1610612739,
    'Detroit Pistons': 1610612765,
    'Indiana Pacers': 1610612754,
    'Miami Heat': 1610612748,
    'Milwaukee Bucks': 1610612749,
    'New York Knicks': 1610612752,
    'Orlando Magic': 1610612753,
    'Philadelphia 76ers': 1610612755,
    'Toronto Raptors': 1610612761,
    'Washington Wizards': 1610612764,
    'Dallas Mavericks': 1610612742,
    'Denver Nuggets': 1610612743,
    'Golden State Warriors': 1610612744,
    'Houston Rockets': 1610612745,
    'Los Angeles Clippers': 1610612746,
    'Los Angeles Lakers': 1610612747,
    'Memphis Grizzlies': 1610612763,
    'Minnesota Timberwolves': 1610612750,
    'New Orleans Pelicans': 1610612740,
    'Oklahoma City Thunder': 1610612760,
    'Phoenix Suns': 1610612756,
    'Portland Trail Blazers': 1610612757,
    'Sacramento Kings': 1610612758,
    'San Antonio Spurs': 1610612759,
    'Utah Jazz': 1610612762,
}
