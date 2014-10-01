from flask import Flask, render_template

app = Flask(__name__)


nba_teams = [
    'Atlanta Hawks',
    'Boston Celtics',
    'Brooklyn Nets',
    'Charlotte Hornets',
    'Chicago Bulls',
    'Cleveland Cavaliers',
    'Detroit Pistons',
    'Indiana Pacers',
    'Miami Heat',
    'Milwaukee Bucks',
    'New York Knicks',
    'Orlando Magic',
    'Philadelphia 76ers',
    'Toronto Raptors',
    'Washington Wizards',
    'Dallas Mavericks',
    'Denver Nuggets',
    'Golden State Warriors',
    'Houston Rockets',
    'Los Angeles Clippers',
    'Los Angeles Lakers',
    'Memphis Grizzlies',
    'Minnesota Timberwolves',
    'New Orleans Pelicans',
    'Oklahoma City Thunder',
    'Phoenix Suns',
    'Portland Trail Blazers',
    'Sacramento Kings',
    'San Antonio Spurs',
    'Utah Jazz',
]


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', nba_teams=nba_teams)

if __name__ == '__main__':
    app.run()
