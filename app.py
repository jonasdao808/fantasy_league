from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import re
from datetime import date
from flask import redirect, url_for, session, flash

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
    admin = db.Column(db.Boolean, default=False)
    

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
    fantasy_points_scored = db.Column(db.Numeric(6), default=0)  # Fantasy points scored by the player
    availability_status = db.Column(db.String(1), default="A")  # Availability status (e.g., 'A' for available)

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

class Trade(db.Model):
    __tablename__ = "trade"
    trade_ID = db.Column(db.Integer, primary_key=True)
    trade_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(64))  # Status of the trade (Pending, Accepted, Rejected)
    proposer = db.Column(db.Integer, db.ForeignKey('team.team_ID'), nullable=False)  # Team proposing the trade
    accepter = db.Column(db.Integer, db.ForeignKey('team.team_ID'), nullable=False)  # Team accepting the trade

    # Relationship to get the team proposing the trade
    proposer_team = db.relationship('Team', foreign_keys=[proposer], backref='proposed_trades')
    # Relationship to get the team accepting the trade
    accepter_team = db.relationship('Team', foreign_keys=[accepter], backref='accepted_trades')

class TradingTeams(db.Model):
    __tablename__ = "trading_teams"
    trade_ID = db.Column(db.Integer, db.ForeignKey('trade.trade_ID'), primary_key=True)
    team_ID = db.Column(db.Integer, db.ForeignKey('team.team_ID'), primary_key=True)

class TradedPlayers(db.Model):
    __tablename__ = "traded_players"
    trade_ID = db.Column(db.Integer, db.ForeignKey('trade.trade_ID'), primary_key=True)
    player_ID = db.Column(db.Integer, db.ForeignKey('player.player_ID'), primary_key=True)
    original_team_ID = db.Column(db.Integer, db.ForeignKey('team.team_ID'), nullable=False)  # Original team of the player

    # Relationship to get the player associated with the trade
    player = db.relationship('Player', backref='traded_players')
    # Relationship to get the original team of the player
    original_team = db.relationship('Team', foreign_keys=[original_team_ID], backref='players_traded')


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
        full_name = request.form['full_name'].strip()
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Validation checks
        if not full_name or not email or not username or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        if len(password) < 4:
            flash('Password must be at least 4 characters long.', 'danger')
            return render_template('register.html')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Invalid email format.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html')

        # Generate a new user ID
        last_user = User.query.order_by(User.user_ID.desc()).first()
        new_user_id = last_user.user_ID + 1 if last_user else 10000000

       

        # Create the new user object
        new_user = User(
            user_ID=new_user_id,
            full_name=full_name,
            email=email,
            username=username,
            password=password
        )

        # Add to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('welcome'))

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
    
    return render_template('home.html', leagues=leagues, is_admin=user.admin)

@app.route('/edit_database')
def edit_database():
    # Ensure only admins can access this page
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user.admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    return render_template('edit_database.html')

@app.route('/edit_players')
def edit_players():
    # Ensure only admins can access this page
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user.admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    # Get all players from the database
    players = Player.query.all()

    return render_template('edit_players.html', players=players)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    # Ensure only admins can access this page
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user.admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Get data from the form
        full_name = request.form['full_name']
        sport = request.form['sport']
        position = request.form['position']
        team = request.form['team']
        fantasy_points_scored = request.form['fantasy_points_scored']

        # Find the highest player_ID in the database
        highest_player_id = db.session.query(db.func.max(Player.player_ID)).scalar()
        # If there are no players, start with 1, otherwise increment the highest player_ID
        new_player_id = highest_player_id + 1 if highest_player_id is not None else 1

        # Create a new Player object with the new player_ID
        new_player = Player(
            player_ID=new_player_id,  # Set player_ID to the next available ID
            full_name=full_name,
            sport=sport,
            position=position,
            team=team,
            fantasy_points_scored=fantasy_points_scored,
            availability_status=request.form.get('availability_status', 'A')  # Default to 'A' if not provided
        )

        # Add the player to the database
        db.session.add(new_player)
        db.session.commit()

        flash(f'Player {full_name} added successfully!', 'success')
        return redirect(url_for('edit_players'))

    return render_template('add_player.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])  # Fetch the logged-in user

    if request.method == 'POST':  # Handle account deletion
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)  # Clear the session
        flash('Your account has been deleted successfully.', 'info')
        return redirect(url_for('welcome'))  # Redirect to the welcome page
    
    return render_template('profile.html', user=user)

@app.route('/waivers')
def waivers():
    # Get the sorting option from the request
    sort = request.args.get('sort', 'name')  # Default sort is 'name'

    # Fetch available players and apply sorting
    if sort == 'position':
        available_players = Player.query.filter_by(availability_status='A').order_by(Player.position).all()
    else:  # Default is sorting by name
        available_players = Player.query.filter_by(availability_status='A').order_by(Player.full_name).all()

    current_team_id = get_current_team_id()
    current_team = Team.query.get(current_team_id)  # Fetch the current team object

    return render_template(
        'waivers.html',
        players=available_players,
        current_team_id=current_team_id,
        team=current_team,  # Pass the team object
        sort=sort  # Pass the current sort option
    )

@app.route('/claim_player/<int:team_id>/<int:player_id>', methods=['GET'])
def claim_player(team_id, player_id):
    player = Player.query.get_or_404(player_id)
    team = Team.query.get_or_404(team_id)

    if not player or player.availability_status != 'A':  # Ensure player is available
        flash('This player is not available for claiming.', "danger")
        return False

    if not team:
        flash("Specified team not found.", "danger")
        return False

    # Mark the player as unavailable
    player.availability_status = 'U'

    # Get the highest draft_ID currently in the database and increment by 1
    max_draft_id = db.session.query(db.func.max(Draft.draft_ID)).scalar() or 0
    new_draft_id = max_draft_id + 1

    # Create a new draft record for this player, linking the player to the team
    new_draft = Draft(
        draft_ID=new_draft_id,
        league_ID=team.league_ID,
        team_ID=team_id,
        player_ID=player_id,
        draft_date=date.today(),
        draft_status='C'
    )
    db.session.add(new_draft)

    # Commit the changes to the database
    db.session.commit()

    flash(f'Player {player.full_name} has been successfully claimed by team {team_id}!', "success")
    return redirect(url_for('team', team_id=team_id))

def get_current_team_id():
    # Get the current user ID from the session
    user_id = session.get('user_id')
    
    if user_id:
        # Fetch the team of the logged-in user (ensure the user owns a team)
        team = Team.query.filter_by(owner=user_id).first()  # Assuming one team per user for now
        if team:
            return team.team_ID
    return None  # Return None if no team is found for the user

def get_current_user_id():
    user_id = session.get("user_id")
    return user_id

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

    # Query players in the team using the drafts table
    players_in_team = db.session.query(Player).join(Draft, Player.player_ID == Draft.player_ID) \
        .filter(Draft.team_ID == team_id).all()

    return render_template('team.html', team=team, matches=matches, players_in_team=players_in_team)

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

@app.route('/drop/<int:league_id>')
def drop_page(league_id):
    current_user = get_current_user_id()

    team = Team.query.filter_by(owner=current_user, league_ID=league_id).first()
    if not team:
        flash("You don't have a team in this league.", "danger")
        return redirect(url_for('league_page', league_id=league_id))
    
    players_in_team = db.session.query(Player).join(Draft, Player.player_ID == Draft.player_ID) \
        .filter(Draft.team_ID == team.team_ID).all()
    return render_template('drop.html', team=team, players=players_in_team)

@app.route('/drop_player/<int:team_id>/<int:player_id>', methods=['POST'])
def drop_player(team_id, player_id):
    team = Team.query.get_or_404(team_id)
    player = Player.query.get_or_404(player_id)

    draft = Draft.query.filter_by(team_ID=team_id, player_ID=player_id).first()
    if draft:
        db.session.delete(draft)

    player.availability_status = 'A'  # Set as available
    db.session.commit()

    flash(f"{player.full_name} has been dropped from team {team_id} and is now available.", "success")
    return redirect(url_for('league_page', league_id=team.league_ID))

@app.route('/propose_new_trade/<int:team_id>', methods=['GET', 'POST'])
def propose_new_trade(team_id):
    # Get the team being traded with
    other_team = Team.query.get_or_404(team_id)

    # Get the current user's team
    current_user_team_id = get_current_team_id()
    current_team = Team.query.get_or_404(current_user_team_id)

    # Get players from both teams
    other_team_players = Player.query.join(Draft).filter(Draft.team_ID == team_id).all()
    current_team_players = Player.query.join(Draft).filter(Draft.team_ID == current_user_team_id).all()

    if request.method == 'POST':
        # Calculate the new trade_ID as max trade_ID + 1
        max_trade_id = db.session.query(db.func.max(Trade.trade_ID)).scalar() or 0
        new_trade_id = max_trade_id + 1

        # Create a new trade record
        new_trade = Trade(trade_ID=new_trade_id, trade_date=date.today(), proposer=current_user_team_id, accepter=team_id, status='Pending')
        db.session.add(new_trade)

        # Add players involved in the trade
        selected_other_team_players = request.form.getlist('other_team_players')
        selected_current_team_players = request.form.getlist('current_team_players')

        for player_id in selected_other_team_players:
            db.session.add(TradedPlayers(trade_ID=new_trade_id, player_ID=player_id, original_team_ID=team_id))
        
        for player_id in selected_current_team_players:
            db.session.add(TradedPlayers(trade_ID=new_trade_id, player_ID=player_id, original_team_ID=current_user_team_id))

        db.session.commit()

        flash('Trade proposal has been sent!', 'success')
        return redirect(url_for('team', team_id=current_user_team_id))

    return render_template(
        'propose_new_trade.html',
        other_team=other_team,
        current_team=current_team,
        other_team_players=other_team_players,
        current_team_players=current_team_players
    )

@app.route('/proposed_trades/<int:league_id>', methods=['GET', 'POST'])
def proposed_trades_page(league_id):
    # Get the current user's team ID
    current_user_team_id = get_current_team_id()
    team = Team.query.get_or_404(current_user_team_id)

    if not current_user_team_id:
        flash("You don't have a team associated with your account.", 'danger')
        return redirect(url_for('home'))

    # Fetch trades where the current user's team is the accepter
    received_trades = (
        db.session.query(Trade)
        .filter_by(accepter=current_user_team_id, status='Pending')
        .all()
    )

    trade_details = []
    for trade in received_trades:
        # Get offered players
        offered_players = (
            db.session.query(Player)
            .join(TradedPlayers, Player.player_ID == TradedPlayers.player_ID)
            .filter(
                TradedPlayers.trade_ID == trade.trade_ID,
                TradedPlayers.original_team_ID == trade.proposer
            )
            .all()
        )

        # Get requested players
        requested_players = (
            db.session.query(Player)
            .join(TradedPlayers, Player.player_ID == TradedPlayers.player_ID)
            .filter(
                TradedPlayers.trade_ID == trade.trade_ID,
                TradedPlayers.original_team_ID == trade.accepter
            )
            .all()
        )

        trade_details.append({
            'trade_id': trade.trade_ID,
            'trade_date': trade.trade_date,
            'offered_players': offered_players,
            'requested_players': requested_players,
            'proposer_team': trade.proposer,
            'accepter_team': trade.accepter
        })

    if request.method == 'POST':
        # Get trade action from form
        trade_id = request.form.get('trade_id')
        action = request.form.get('action')

        trade = Trade.query.get(trade_id)

        if not trade or trade.status != 'Pending':
            flash("Trade not found or already processed.", "danger")
            return redirect(url_for('proposed_trades_page'))

        if action == 'accept':
            # Swap players between teams
            offered_players = (
                db.session.query(TradedPlayers.player_ID)
                .filter(TradedPlayers.trade_ID == trade_id, TradedPlayers.original_team_ID == trade.proposer)
                .all()
            )

            requested_players = (
                db.session.query(TradedPlayers.player_ID)
                .filter(TradedPlayers.trade_ID == trade_id, TradedPlayers.original_team_ID == trade.accepter)
                .all()
            )

            # Perform swaps
            for player_id, in offered_players:
                # Drop from proposer and claim by accepter
                drop_player(trade.proposer, player_id)
                claim_player(trade.accepter, player_id)

            for player_id, in requested_players:
                # Drop from accepter and claim by proposer
                drop_player(trade.accepter, player_id)
                claim_player(trade.proposer, player_id)

            trade.status = 'Accepted'
            db.session.commit()
            flash("Trade accepted successfully!", "success")
            return redirect(url_for("league_page", league_id=league_id))

        elif action == 'reject':
            trade.status = 'Rejected'
            db.session.commit()
            flash("Trade rejected successfully!", "info")
            return redirect(url_for("league_page", league_id=league_id))

        else:
            flash("Invalid action.", "danger")

        return render_template('proposed_trades.html', trades=trade_details, team=team)

    return render_template('proposed_trades.html', trades=trade_details, team=team)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=True)
