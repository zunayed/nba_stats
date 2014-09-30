import io
import re
import json

import requests


def parse_data(team, team_id):
    """
    Save data from every game for given team
    """
    print "Parsing data for %s" % team
    url = "http://stats.nba.com/stats/" \
        "teamgamelog?Season=2013-14&SeasonType=Regular+Season&LeagueID=00&TeamID=%d" \
        "&pageNo=1&rowsPerPage=100" % team_id

    response = requests.get(url)
    data = json.loads(response.content)['resultSets'][0]

    stat_keys = data['headers']
    individual_game_stats = data['rowSet']

    games_data = {}

    for game in individual_game_stats:
        # u'NYK @ HOU' -> HOS
        team_vs = re.sub('[@, vs , .]', '', game[3][4:])

        if team_vs not in games_data:
            games_data[team_vs] = [dict(zip(stat_keys, game))]

        games_data[team_vs].append(dict(zip(stat_keys, game)))

    return games_data


def average_data(data):
    avg_data = {}
    fields_to_average = ['FG_PCT', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
                         'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB',
                         'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

    for team_vs in data:
        avg_data[team_vs] = {}
        for field in fields_to_average:
            total = 0
            for game in data[team_vs]:
                total += game[field]

            avg_data[team_vs][field] = total / len(data[team_vs])

    return avg_data


def get_teams_data():
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
    league_data = {}

    for team, team_id in nba_team_ids.iteritems():
        league_data[team] = parse_data(team, team_id)

    league_data_averaged = {}

    for team in league_data:
        league_data_averaged[team] = average_data(league_data[team])

    with io.open('league_data.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(league_data, ensure_ascii=False)))

    with io.open('league_data_averaged.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(league_data_averaged, ensure_ascii=False)))


geo_nba_teams = {
    'MIL': (43.043694, -87.91713),
    'MIN': (44.979549, -93.276131),
    'MIA': (25.781233, -80.18782),
    'ATL': (33.7569923, -84.3919983),
    'BOS': (42.3663175, -71.0597084),
    'DET': (42.6963466, -83.2440995),
    'DEN': (39.7473979, -105.007974),
    'SAC': (38.6481556, -121.5210461),
    'BKN': (40.683281, -73.976181),
    'POR': (45.5314969, -122.6667829),
    'ORL': (28.5389544, -81.3842762),
    'TOR': (43.6434402, -79.3789597),
    'CHI': (41.880394, -87.673164),
    'SAS': (29.4251727, -98.4349231),
    'CHA': (35.225163, -80.839302),
    'CLE': (41.5047493, -81.6907196),
    'WAS': (38.898125, -77.02095),
    'LAL': (34.043125, -118.267097),
    'PHI': (39.9052513, -75.1734781),
    'MEM': (35.1394768, -90.0516909),
    'LAC': (34.0417841, -118.2670411),
    'DAL': (32.790302, -96.810219),
    'OKC': (35.463402, -97.514984),
    'PHX': (33.4459, -112.071312),
    'IND': (39.764046, -86.15551),
    'NOP': (29.9440784, -90.083168),
    'HOU': (29.7519596, -95.3622159)
}

get_teams_data()
