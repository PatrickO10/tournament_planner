-- Table definitions for the tournament project.

-- Remove tournament database.
DROP DATABASE tournament;

-- Creating the tournament database and establishing the schema
CREATE DATABASE tournament;

-- Connect to newly created database.
\c tournament;

-- Creates a `Players` table with a primary id and a name.
CREATE TABLE Players (
	id serial PRIMARY KEY,
	name text
);

-- Creates a 'Matches' table with a primary id and
-- defined foreign keys for winner and loser to make sure
-- only the `Players.id` can be inserted.
CREATE TABLE Matches (
	id serial PRIMARY KEY,
	winner_id int REFERENCES Players(id),
	loser_id int REFERENCES Players(id)
);

-- Creates a view that shows how many matches each player has played.
CREATE VIEW v_matchesPlayed AS
	SELECT
		Players.id as player_id,
		Players.name as player_name,
		COUNT(Matches.id) AS matches_played
	FROM Players LEFT JOIN Matches
	ON Matches.winner_id = Players.id OR Matches.loser_id = Players.id
	GROUP BY Players.id;

-- Creates a view that shows the number of wins for each player.
CREATE VIEW v_wins AS
	SELECT
		Players.id,
		Players.name,
		COUNT(Matches.winner_id) AS wins
	FROM Players LEFT JOIN Matches
	ON Matches.winner_id = Players.id
	GROUP BY Players.id
	ORDER BY wins DESC;

-- Creates a view that shows the players standings.
CREATE VIEW v_standings AS
	SELECT
		v_wins.id,
		v_wins.name,
		v_wins.wins,
		v_matchesPlayed.matches_played
	FROM v_wins LEFT JOIN v_matchesPlayed
	ON v_wins.id = v_matchesPlayed.player_id
	ORDER BY v_wins.wins DESC;


/*
-- Inserts for testing purposes.
-- Players
INSERT INTO Players (name) VALUES('ADAM APPLE');
INSERT INTO Players (name) VALUES('BLAKE BOMB');
INSERT INTO Players (name) VALUES('CARL CALM');
INSERT INTO Players (name) VALUES('DAN DOM');
INSERT INTO Players (name) VALUES('EVAN EVIL');
INSERT INTO Players (name) VALUES('FLAMING FIRE');
INSERT INTO Players (name) VALUES('GLARING GULL');
INSERT INTO Players (name) VALUES('HILLARY HILLY');

-- Round 1
INSERT INTO Matches (winner_id, loser_id) VALUES(1, 2);
INSERT INTO Matches (winner_id, loser_id) VALUES(3, 4);
INSERT INTO Matches (winner_id, loser_id) VALUES(5, 6);
INSERT INTO Matches (winner_id, loser_id) VALUES(7, 8);


-- Round 2
INSERT INTO Matches (winner_id, loser_id) VALUES(1, 3);
INSERT INTO Matches (winner_id, loser_id) VALUES(4, 2);
INSERT INTO Matches (winner_id, loser_id) VALUES(5, 7);
INSERT INTO Matches (winner_id, loser_id) VALUES(6, 8);

-- Round 3
INSERT INTO Matches (winner_id, loser_id) VALUES(1, 5);
INSERT INTO Matches (winner_id, loser_id) VALUES(3, 4);
INSERT INTO Matches (winner_id, loser_id) VALUES(6, 7);
INSERT INTO Matches (winner_id, loser_id) VALUES(8, 2);

-- Round 4
INSERT INTO Matches (winner_id, loser_id) VALUES(1, 5);
INSERT INTO Matches (winner_id, loser_id) VALUES(3, 6);
INSERT INTO Matches (winner_id, loser_id) VALUES(7, 4);
INSERT INTO Matches (winner_id, loser_id) VALUES(8, 2);
*/