from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hailee_yatin_jonas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/fantasy'
# username = root
# mysql:host=localhost;dbname=fantasy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# path to python
# TO RUN APP:  C:\Users\haile\AppData\Local\Programs\Python\Python313\python.exe app.py

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()  # This creates tables based on your models

class User(db.Model):
    __tablename__ = 'user'  # This tells SQLAlchemy to use the existing 'user' table
    user_ID = db.Column(db.Integer, primary_key=True)  # user_ID as primary key
    full_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    profile_settings = db.Column(db.String(64))

class League(db.Model):
    __tablename__ = 'league'
    league_ID = db.Column(db.Numeric(8), primary_key=True)  # Numeric type for league ID
    league_name = db.Column(db.String(30), nullable=False)
    league_type = db.Column(db.String(1), default='U')  # Default 'U' for the league type
    commissioner = db.Column(db.String(20), db.ForeignKey('user.username'))  # Foreign key referencing the user table
    max_teams = db.Column(db.Integer, nullable=False, default=10)  # Default maximum number of teams
    draft_date = db.Column(db.Date)  # Date field for the draft date

    # Relationship with the User model (one-to-many)
    commissioner_user = db.relationship('User', backref=db.backref('leagues', lazy=True))

    def __repr__(self):
        return f'<League {self.league_name} ({self.league_ID})>'
    
class Team(db.Model):
    __tablename__ = 'team'
    team_ID = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    league_ID = db.Column(db.Integer, db.ForeignKey('league.league_ID'), nullable=False)  # Foreign key to League
    owner = db.Column(db.Integer, db.ForeignKey('user.user_ID'), nullable=False)  # Change to 'owner' to match your DB schema
    status = db.Column(db.String(1), nullable=False)
    total_points_scored = db.Column(db.Integer)
    league_ranking = db.Column(db.Integer)
    
    # Relationship with League (many-to-one)
    league = db.relationship('League', backref=db.backref('teams', lazy=True))
    
    # Relationship with User (many-to-one)
    owner_user = db.relationship('User', backref=db.backref('teams', lazy=True))  # This is the relationship with the User model

    def __repr__(self):
        return f'<Team {self.team_name} ({self.team_ID})>'
    
class Player(db.Model):
    __tablename__ = 'player'

    player_ID = db.Column(db.Numeric(8), primary_key=True)  # Primary key for player
    full_name = db.Column(db.String(50), nullable=False)  # Player's full name
    sport = db.Column(db.String(3), nullable=False)  # Sport type (e.g., 'NFL', 'NBA')
    position = db.Column(db.String(3), nullable=False)  # Position (e.g., 'QB', 'RB')
    team = db.Column(db.String(50), nullable=False)  # The team the player is associated with
    fantasy_points_scored = db.Column(db.Numeric(6))  # Fantasy points scored by the player
    availability_status = db.Column(db.String(1))  # Availability status (e.g., 'A' for active)

    def __repr__(self):
        return f'<Player {self.full_name} ({self.player_ID})>'

class Draft(db.Model):
    __tablename__ = 'drafts'

    draft_ID = db.Column(db.Numeric(8), primary_key=True)  # Primary key for draft
    league_ID = db.Column(db.Numeric(8), db.ForeignKey('league.league_ID'), nullable=False)  # Foreign key to League
    team_ID = db.Column(db.Integer, db.ForeignKey('team.team_ID'), nullable=False)  # Foreign key to Team
    player_ID = db.Column(db.Numeric(8), db.ForeignKey('player.player_ID'), nullable=False)  # Foreign key to Player
    draft_date = db.Column(db.Date)  # The date the draft took place
    draft_order = db.Column(db.String(1))  # Draft order (e.g., '1' for first pick)
    draft_status = db.Column(db.String(1))  # Draft status (e.g., 'C' for completed)

    # Relationships
    player = db.relationship('Player', backref=db.backref('drafts', lazy=True))
    league = db.relationship('League', backref=db.backref('drafts', lazy=True))
    team = db.relationship('Team', backref=db.backref('drafts', lazy=True))

    def __repr__(self):
        return f'<Draft {self.draft_ID} - League {self.league_ID} - Team {self.team_ID} - Player {self.player_ID}>'

class GameMatch(db.Model):
    __tablename__ = 'game_match'
    match_ID = db.Column(db.Numeric(8), primary_key=True)
    match_date = db.Column(db.Date)
    final_score = db.Column(db.String(10))
    winner = db.Column(db.Numeric(8), db.ForeignKey('team.team_ID'))

class MatchSchedule(db.Model):
    __tablename__ = 'match_schedule'
    match_ID = db.Column(db.Numeric(8), db.ForeignKey('game_match.match_ID'), primary_key=True)
    team_ID = db.Column(db.Numeric(8), db.ForeignKey('team.team_ID'), primary_key=True)

class MatchEvent(db.Model):
    __tablename__ = 'match_event'
    match_event_ID = db.Column(db.Numeric(10), primary_key=True)
    player_ID = db.Column(db.Numeric(8), db.ForeignKey('player.player_ID'))
    match_ID = db.Column(db.Numeric(8), db.ForeignKey('game_match.match_ID'))
    event_type = db.Column(db.String(20))
    event_time = db.Column(db.Time)
    fantasy_points = db.Column(db.Numeric(6))



# Routes
@app.route('/', methods=['GET', 'POST'])
def welcome():
    leagues = League.query.all()  # Get all the leagues from the database
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password matches
        if user and user.password==password:
            # Store the user ID in the session
            session['user_id'] = user.user_ID  # Save user ID to session
            
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home page
        else:
            flash('Username or password is incorrect.', 'warning')
            return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    # Get the user by the ID stored in the session
    user = User.query.get(session['user_id'])
    
    # Get all teams that the user is part of, based on 'owner' (the correct column name in the DB)
    user_teams = Team.query.filter_by(owner=user.user_ID).all()  # Using 'owner' instead of 'user_ID'

    # Get the leagues associated with these teams
    leagues = [team.league for team in user_teams]
    
    return render_template('home.html', leagues=leagues)

@app.route('/league/<int:league_id>')
def league_page(league_id):
    # Fetch the league by ID
    league = League.query.get(league_id)

    if not league:
        flash('League not found.', 'danger')
        return redirect(url_for('home'))  # Redirect back to home page if league doesn't exist

    # Get all teams in this league
    teams = Team.query.filter_by(league_ID=league_id).all()

    return render_template('league.html', league=league, teams=teams)



@app.route('/team/<int:team_id>')
def team(team_id):
    # Fetch the team details
    team = Team.query.get_or_404(team_id)

    # Query matches involving this team using the match_schedule table
    matches = db.session.query(GameMatch).join(MatchSchedule, GameMatch.match_ID == MatchSchedule.match_ID) \
        .filter(MatchSchedule.team_ID == team_id).all()

    return render_template('team.html', team=team, matches=matches)

@app.route('/match/<int:match_id>')
def match(match_id):
    # Fetch the match details
    match = GameMatch.query.get_or_404(match_id)

    # Fetch the teams involved in this match
    teams = db.session.query(Team).join(MatchSchedule, Team.team_ID == MatchSchedule.team_ID) \
        .filter(MatchSchedule.match_ID == match_id).all()

    # Separate players by team
    team1_players = db.session.query(Player).join(Draft, Player.player_ID == Draft.player_ID) \
        .filter(Draft.team_ID == teams[0].team_ID).all()
    team2_players = db.session.query(Player).join(Draft, Player.player_ID == Draft.player_ID) \
        .filter(Draft.team_ID == teams[1].team_ID).all()

    # Fetch events linked to this match
    events = MatchEvent.query.filter_by(match_ID=match_id).all()

    return render_template(
        'match.html',
        match=match,
        teams=teams,
        team1_players=team1_players,
        team2_players=team2_players,
        events=events
    )


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)
