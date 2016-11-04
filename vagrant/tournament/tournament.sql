-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;


CREATE DATABASE tournament;


\c tournament;


CREATE TABLE Players (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);


CREATE TABLE Matches (
	id SERIAL PRIMARY KEY,
	player1 INT NOT NULL REFERENCES Players (id),
	player2 INT NOT NULL REFERENCES Players (id),
	winner INT NOT NULL
);


CREATE VIEW wins_count AS
	(SELECT Players.id, Name AS name, count(Matches.id) AS wins, CASE WHEN EXISTS (SELECT 1 FROM Matches) THEN 
										(SELECT count(*) FROM Matches 
									 		WHERE player1 = Players.id 
										 	   OR player2 = Players.id)
									        ELSE 0 
								     END AS matches
		FROM Players LEFT JOIN Matches
		ON Players.id = winner
		GROUP BY Players.id, Name
		ORDER BY wins DESC);

