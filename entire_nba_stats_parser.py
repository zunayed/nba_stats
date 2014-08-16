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

    with io.open('league_data.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(league_data, ensure_ascii=False)))


def average_data(games):
    pass


get_teams_data()
