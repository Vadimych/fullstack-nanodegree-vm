-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament;

DELETE FROM Players;
DELETE FROM Matches;

ALTER SEQUENCE Players_id_seq RESTART;
ALTER SEQUENCE Matches_id_seq RESTART;

INSERT INTO Players (Name)
	VALUES ('Vadym'),
		   ('Maxim'),
		   ('Vitamino'),
		   ('Rost');

INSERT INTO Matches (round, player1, player2, winner)
	VALUES (1, 1, 2, 1),
		   (1, 3, 4, 3),
		   (2, 1, 3, 1),
		   (2, 2, 4, 2);
		   
SELECT * FROM Players;
SELECT * FROM Matches;


CREATE VIEW wins_count AS
	(SELECT Name, count(Matches.id) as wins
		FROM Players LEFT JOIN Matches
		ON (player1 = winner
			AND player1 = Players.id)
			OR (player2 = winner
			AND player2 = Players.id)
		GROUP BY Name
		ORDER BY wins DESC);

SELECT * FROM wins_count;
	
	