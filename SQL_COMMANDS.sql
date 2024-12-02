
DROP TABLE IF EXISTS user;
CREATE TABLE user (
	user_ID NUMERIC(8),
	full_name VARCHAR(50), 
	email VARCHAR(50) UNIQUE NOT NULL, 
	username VARCHAR(20) UNIQUE NOT NULL,
	password VARCHAR(64) NOT NULL,
	profile_settings VARCHAR(64),
	PRIMARY KEY(user_ID)
);

CREATE TABLE player (
    player_ID NUMERIC(8),
    full_name VARCHAR(50),
    sport CHAR(3),
    position CHAR(3),
    team VARCHAR(50),
    fantasy_points_scored NUMERIC(6),
    availability_status CHAR(1),
    PRIMARY KEY(player_ID)
	);

CREATE TABLE league (
	league_ID NUMERIC(8),
	league_name VARCHAR(30) NOT NULL,
	league_type CHAR(1) DEFAULT 'U',
	commissioner VARCHAR(20),
	FOREIGN KEY (commissioner) REFERENCES user(username),
	max_teams INT NOT NULL DEFAULT 10,
	draft_date DATE,
	PRIMARY KEY(league_ID)
);

CREATE TABLE team (
    team_ID NUMERIC(8) PRIMARY KEY,
    owner NUMERIC(8),
    league_ID NUMERIC(8),
    total_points_scored NUMERIC(6),
    league_ranking NUMERIC(3),
    team_name VARCHAR(25),
    status CHAR(1),
    FOREIGN KEY (owner) REFERENCES user(user_ID),
    FOREIGN KEY (league_ID) REFERENCES league(league_ID)
);


CREATE TABLE trade (
    trade_ID NUMERIC(10) PRIMARY KEY,
    trade_date DATE
);



CREATE TABLE drafts (
	draft_ID NUMERIC(8),
	league_ID NUMERIC(8),
	player_ID NUMERIC(8),
	FOREIGN KEY (league_ID) REFERENCES league(league_ID),
	FOREIGN KEY (player_ID) REFERENCES player(player_ID),
	draft_date DATE,
	draft_order CHAR(1), 
	draft_status CHAR(1),
	PRIMARY KEY(draft_ID)
);

CREATE TABLE traded_players (
	trade_ID NUMERIC(10),
	player_ID NUMERIC(8),
	FOREIGN KEY(trade_ID) REFERENCES trade(trade_ID),
	FOREIGN KEY(player_ID) REFERENCES player(player_ID),
	PRIMARY KEY (trade_ID, player_ID)
);

CREATE TABLE game_match (
    match_ID NUMERIC(8) PRIMARY KEY,
    match_date DATE,
    final_score VARCHAR(10),
    winner NUMERIC(8)
);


CREATE TABLE player_statistic (
    statistic_ID NUMERIC(10),  
    player_ID NUMERIC(8), 
    game_date DATE,
    performance_stats TEXT,  
    injury_status CHAR(1) DEFAULT 'N',
    PRIMARY KEY (statistic_ID),
    FOREIGN KEY (player_ID) REFERENCES player(player_ID) 
);


CREATE TABLE waiver (
    waiver_ID NUMERIC(8),
    team_ID NUMERIC(8),
    player_ID NUMERIC(8),
    waiver_order INT(3),
    waiver_status CHAR(1) DEFAULT 'P',
    waiver_pick_up_date DATE,
    PRIMARY KEY (waiver_ID),
    FOREIGN KEY (team_ID) REFERENCES team(team_ID),
    FOREIGN KEY (player_ID) REFERENCES player(player_ID)
);

CREATE TABLE match_event (
    match_event_ID NUMERIC(10),
    player_ID NUMERIC(8) REFERENCES player(player_ID),
    match_ID NUMERIC(8) REFERENCES game_match(match_ID),
    event_type VARCHAR(20),
    event_time TIME,
    fantasy_points NUMERIC(6),
    PRIMARY KEY(match_event_ID)
);


CREATE TABLE match_schedule (
   match_ID NUMERIC(8),
   team_ID NUMERIC(8),
   PRIMARY KEY (match_ID, team_ID),
   FOREIGN KEY (team_ID) REFERENCES team(team_ID),
   FOREIGN KEY (match_ID) REFERENCES game_match(match_ID)
);


CREATE TABLE trading_teams (
   trade_ID NUMERIC(10),
   team_ID NUMERIC(8),
   FOREIGN KEY (team_ID) REFERENCES team(team_ID),
   FOREIGN KEY (trade_ID) REFERENCES trade(trade_ID),
   PRIMARY KEY (trade_ID, team_ID)

);

INSERT INTO user (user_ID, full_name, email, username, password, profile_settings) VALUES
(10000001, 'Yatin Marpu', 'ymarpu@gmail.com', 'ymarpu', 'hashed_pw1', 'Notifications: ON'),
(10000002, 'Hailee Yun', 'hyun@gmaill.com', 'hyun', 'hashed_pw2', 'Notifications: ON'),
(10000003, 'Jonas Dao', 'jdao@gmail.com', 'jdao', 'hashed_pw3', 'Notifications: ON'),
(10000004, 'Salim Arfaoui', 'sarfaoui@gmail.com', 'sarfouai', 'hashed_pw4', 'Notifications: ON'),
(10000005, 'Dani Smolka', 'dsmolka@gmail.com', 'dsmolka', 'hashed_pw5', 'Notifications: ON'),
(10000006, 'Ryan Wong', 'rwong@gmail.com', 'rwong', 'hashed_pw6', 'Notifications: ON'),
(10000007, 'Farabi Azad', 'fazad@gmail.com', 'fazad', 'hashed_pw7', 'Notifications: ON'),
(10000008, 'Lorrie Savage', 'lsavage@gmail.com', 'lsavage', 'hashed_pw8', 'Notifications: ON'),
(10000009, 'Siam Huda', 'shuda@gmail.com', 'shuda', 'hashed_pw9', 'Notifications: ON'),
(10000010, 'Haesun Uhm', 'huhm@gmail.com', 'huhm', 'hashed_pw10', 'Notifications: ON');

INSERT INTO player (player_ID, full_name, sport, position, team, fantasy_points_scored, availability_status) VALUES
(20000001, 'Justin Jefferson', 'FTB', 'WR', 'Vikings', 300.5, 'U'),
(20000002, 'Tyreek Hill', 'FTB', 'WR', 'Dolphins', 250.0, 'A'),
(20000003, 'James Connor', 'FTB', 'RB',  'Cardinals', 275.5, 'A'),
(20000004, 'Saquon Barkley', 'FTB', 'RB', 'Eagles', 340.5, 'A'),
(20000005, 'Dak Prescott', 'FTB', 'QB', 'Cowboys', 245.0, 'A'),
(20000006, 'Patrick Mahomes', 'FTB', 'QB', 'Chiefs', 310.5, 'A'),
(20000007, 'Jordan Love', 'FTB', 'QB', 'Packers', 230.0, 'A'),
(20000008, 'D’Andre Smith', 'FTB', 'RB', 'Bears', 260.0, 'A'),
(20000009, 'Aaron Rodgers', 'FTB', 'QB', 'Jets', 295.5, 'A'),
(20000010, 'Chuba Hubbard', 'FTB', 'RB', 'Panthers', 270.0, 'A'),
(20000011, 'Justin Herbert', 'FTB', 'QB', 'Chargers', 200.0, 'A'),
(20000012, 'Joe Burrow', 'FTB', 'QB', 'Bengals', 310.0, 'A'),
(20000013, 'Mark Andrews', 'FTB', 'TE',  'Ravens', 75.5, 'A'),
(20000014, 'Jalen Hurts', 'FTB', 'QB', 'Eagles', 140.5, 'A'),
(20000015, 'Sam LaPorta', 'FTB', 'TE', 'Lions', 145.0, 'A'),
(20000016, 'Travis Kelce', 'FTB', 'TE', 'Chiefs', 340.0, 'A'),
(20000017, 'Derrick Henry', 'FTB', 'RB', 'Ravens', 250.0, 'A'),
(20000018, 'Keenan Allen', 'FTB', 'WR', 'Bears', 230.0, 'A'),
(20000019, 'Jayden Daniels', 'FTB', 'QB', 'Commanders', 395.0, 'A'),
(20000020, 'Allen Lazard', 'FTB', 'WR', 'Jets', 100.0, 'A');

INSERT INTO league (league_ID, league_name, league_type, commissioner, max_teams, draft_date) VALUES
(30000001, 'Yatin’s League', 'U', 'ymarpu', 10, '2024-08-21'),
(30000002, 'Hailee’s League', 'P', 'hyun', 10, '2024-08-22'),
(30000003, 'Jonas’s League', 'R', 'jdao', 12, '2024-08-23'),
(30000004, 'Professor’s League', 'U', 'sarfouai', 16, '2024-08-14'),
(30000005, 'Danielle’s League', 'P', 'dsmolka', 10, '2024-08-25'),
(30000006, 'Ryan’s League', 'R', 'rwong', 12, '2024-08-26'),
(30000007, 'Farabi’s League', 'U', 'fazad', 14, '2024-09-15'),
(30000008, 'Lorrie’s League', 'P', 'lsavage', 8, '2024-09-30'),
(30000009, 'Siam’s League', 'R', 'shuda', 10, '2024-08-20'),
(30000010, 'Haesun’s League', 'U', 'huhm', 12, '2024-09-18');

INSERT INTO team (team_ID, owner, league_ID, total_points_scored, league_ranking, team_name, status) VALUES
(40000001, 10000001, 30000001, 850.0, 1, 'Yatin’s Team', 'A'),
(40000002, 10000002, 30000001, 780.0, 2, 'Hailee’s Team', 'A'),
(40000003, 10000003, 30000001, 900.0, 1, 'Jonas’s Team', 'A'),
(40000004, 10000004, 30000001, 760.0, 2, 'Professor’s Team', 'A'),
(40000005, 10000005, 30000001, 800.0, 3, 'Danielle’s Team', 'A'),
(40000006, 10000006, 30000001, 820.0, 1, 'Ryan’s Team', 'A'),
(40000007, 10000007, 30000001, 830.0, 2, 'Farabi’s Team', 'A'),
(40000008, 10000008, 30000001, 750.0, 3, 'Lorrie’s Team', 'A'),
(40000009, 10000009, 30000001, 810.0, 1, 'Siam’s Team', 'A'),
(40000010, 10000010, 30000001, 760.0, 2, 'Haesun’s Team', 'A');

INSERT INTO trade (trade_ID, trade_date) VALUES
(5000000001, '2024-11-01'),
(5000000002, '2024-11-02'),
(5000000003, '2024-11-03'),
(5000000004, '2024-11-04'),
(5000000005, '2024-11-05'),
(5000000006, '2024-11-06'),
(5000000007, '2024-11-07'),
(5000000008, '2024-11-08'),
(5000000009, '2024-11-09'),
(5000000010, '2024-11-10');

INSERT INTO traded_players (trade_ID, player_ID) VALUES
(5000000001, 20000001),
(5000000001, 20000002),
(5000000002, 20000003),
(5000000002, 20000004),
(5000000003, 20000005),
(5000000003, 20000006),
(5000000004, 20000007),
(5000000004, 20000008),
(5000000005, 20000009),
(5000000005, 20000010);

INSERT INTO trading_teams (trade_ID, team_ID) VALUES
(5000000001, 40000001),
(5000000001, 40000002),
(5000000002, 40000003),
(5000000002, 40000004),
(5000000003, 40000005),
(5000000003, 40000006),
(5000000004, 40000007),
(5000000004, 40000008),
(5000000005, 40000009),
(5000000005, 40000010);

INSERT INTO game_match (match_ID, match_date, final_score, winner) VALUES
(60000001, '2024-10-01', '28-21', 40000001),
(60000002, '2024-10-02', '35-30', 40000002),
(60000003, '2024-10-03', '14-20', 40000004),
(60000004, '2024-10-04', '22-18', 40000004),
(60000005, '2024-10-05', '17-24', 40000006),
(60000006, '2024-10-06', '27-27', NULL),
(60000007, '2024-10-07', '32-28', 40000007),
(60000008, '2024-10-08', '40-38', 40000008),
(60000009, '2024-10-09', '21-15', 40000009),
(60000010, '2024-10-10', '18-22', 40000001);

INSERT INTO match_event (match_event_ID, player_ID, match_ID, event_type, event_time, fantasy_points) VALUES
(7000000001, 20000001, 60000001, 'Touchdown', '01:05:30', 6.0),
(7000000002, 20000002, 60000002, 'Field Goal', '02:10:45', 3.0),
(7000000003, 20000003, 60000003, 'Touchdown', '03:15:20', 10.0),
(7000000004, 20000004, 60000004, 'Interception', '04:22:10', 4.0),
(7000000005, 20000005, 60000005, 'Touchdown', '05:30:00', 6.0),
(7000000006, 20000006, 60000006, 'Field Goal', '06:40:30', 3.0),
(7000000007, 20000007, 60000007, 'Interception', '07:50:15', 10.0),
(7000000008, 20000008, 60000008, 'Touchdown', '08:20:10', 3.0),
(7000000009, 20000009, 60000009, 'Field Goal', '09:20:05', 4.0),
(7000000010, 20000010, 60000010, 'Touchdown', '10:10:00', 6.0);

INSERT INTO match_schedule (match_ID, team_ID) VALUES
(60000001, 40000001),
(60000001, 40000002),
(60000002, 40000003),
(60000002, 40000004),
(60000003, 40000005),
(60000003, 40000006),
(60000004, 40000007),
(60000004, 40000008),
(60000005, 40000009),
(60000005, 40000010);

-- i got rid of this one because i wanted to add a team_ID column
-- INSERT INTO drafts (draft_ID, league_ID, player_ID, draft_date, draft_order, draft_status) VALUES
-- (80000001, 30000001, 20000020, '2024-11-01', 'R', 'C'),
-- (80000002, 30000002, 20000011, '2024-11-02', 'S', 'I'),
-- (80000003, 30000003, 20000012, '2024-11-03', 'R', 'C'),
-- (80000004, 30000004, 20000013, '2024-11-04', 'S', 'C'),
-- (80000005, 30000005, 20000014, '2024-11-05', 'R', 'I'),
-- (80000006, 30000006, 20000015, '2024-11-06', 'S', 'C'),
-- (80000007, 30000007, 20000016, '2024-11-07', 'R', 'I'),
-- (80000008, 30000008, 20000017, '2024-11-08', 'S', 'C'),
-- (80000009, 30000009, 20000018, '2024-11-09', 'R', 'I'),
-- (80000010, 30000010, 20000019,  '2024-11-10', 'S', 'C');

-- new one
INSERT INTO drafts (draft_ID, league_ID, team_ID, player_ID, draft_date, draft_order, draft_status) VALUES
(80000001, 30000001, 40000001, 20000020, '2024-11-01', 'R', 'C'),
(80000002, 30000002, 40000002, 20000011, '2024-11-02', 'S', 'I'),
(80000003, 30000003, 40000003, 20000012, '2024-11-03', 'R', 'C'),
(80000004, 30000004, 40000004, 20000013, '2024-11-04', 'S', 'C'),
(80000005, 30000005, 40000005, 20000014, '2024-11-05', 'R', 'I'),
(80000006, 30000006, 40000006, 20000015, '2024-11-06', 'S', 'C'),
(80000007, 30000007, 40000007, 20000016, '2024-11-07', 'R', 'I'),
(80000008, 30000008, 40000001, 20000017, '2024-11-08', 'S', 'C'),
(80000009, 30000009, 40000002, 20000018, '2024-11-09', 'R', 'I'),
(80000010, 30000010, 40000003, 20000019, '2024-11-10', 'S', 'C');

-- i then added 2 more columns to the draft table


INSERT INTO waiver (waiver_ID, team_ID, player_ID, waiver_order, waiver_status, waiver_pick_up_date) VALUES
(90000001, 40000001, 20000001, 1, 'A', '2024-11-05'),
(90000002, 40000002, 20000002, 2, 'P', NULL),
(90000003, 40000003, 20000003, 3, 'A', '2024-11-06'),
(90000004, 40000004, 20000004, 4, 'P', NULL),
(90000005, 40000005, 20000005, 5, 'A', '2024-11-07'),
(90000006, 40000006, 20000006, 6, 'P', NULL),
(90000007, 40000007, 20000007, 7, 'A', '2024-11-08'),
(90000008, 40000008, 20000008, 8, 'P', NULL),
(90000009, 40000009, 20000009, 9, 'A', '2024-11-09'),
(90000010, 40000010, 20000010, 10, 'P', NULL);


INSERT INTO player_statistic (statistic_ID, player_ID, game_date, performance_stats, injury_status) VALUES
(1000000001, 20000001, '2024-10-01', 'TD: 2; Yards: 300', 'N'),
(1000000002, 20000002, '2024-10-02', 'FG: 1; Yards: 48', 'N'),
(1000000003, 20000003, '2024-10-03', 'TD: 1; Yards: 40', 'N'),
(1000000004, 20000004, '2024-10-04', 'FG: 2; Yards: 13',  'N'),
(1000000005, 20000005, '2024-10-05', 'TD: 1; Yards: 125', 'N'),
(1000000006, 20000006, '2024-10-06', 'FG: 25; Yards: 5', 'Y'),
(1000000007, 20000007, '2024-10-07', 'INT: 3; Yards: 1', 'N'),
(1000000008, 20000008, '2024-10-08', 'TD: 3; Yards: 200', 'Y'),
(1000000009, 20000009, '2024-10-09', 'FG: 28; Yards: 12', 'N'),
(1000000010, 20000010, '2024-10-10', 'TD: 5; Yards: 40', 'N');


SELECT * FROM user;
SELECT full_name 
FROM player 
WHERE position = ‘QB’;

SELECT *
FROM match_schedule
WHERE team_ID = ‘40000004’;

SELECT game_match.match_date, game_match.final_score
FROM game_match
JOIN match_event
ON match_event.match_ID = game_match.match_ID
WHERE match_event.player_ID = ‘40000003’;

UPDATE player
SET availability_status = 'A'
WHERE player_ID = 20000009;

UPDATE league
SET league_type = 'P'
WHERE league_ID = 30000001;

UPDATE team
SET status = 'U'
WHERE team_ID = 40000010;

DELETE FROM league
WHERE league_ID IN (30000008, 30000009);


CREATE TRIGGER update_player_availability_after_draft
AFTER INSERT ON drafts
FOR EACH ROW
BEGIN
    UPDATE player
    SET availability_status = 'U'
    WHERE player_ID = NEW.player_ID;
END @@

DELIMITER ;



DELIMITER $$

CREATE PROCEDURE available_players()
BEGIN
    SELECT *
    FROM player
    WHERE availability_status = 'A';
END $$

DELIMITER ;

CALL available_players();
