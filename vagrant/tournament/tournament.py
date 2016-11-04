#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def queryToDatabase(*query):
    """Execute query to the Database"""
    conn = connect()
    c = conn.cursor()

    if len(query) > 1:
        c.execute(query[0], query[1])
    else:
        c.execute(query[0])

    try:
        query_result = c.fetchall()
        conn.commit() 
        conn.close()
        return query_result

    except psycopg2.ProgrammingError:
        conn.commit() 
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    queryToDatabase("DELETE FROM Matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    queryToDatabase("DELETE FROM Players;")


def countPlayers():
    """Returns the number of players currently registered."""    
    res = queryToDatabase("SELECT count(*) FROM Players;")
    count = res[0][0]
    return int(count)


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    queryToDatabase("INSERT INTO Players (Name) VALUES (%s);", (bleach.clean(name), ))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    res = queryToDatabase("SELECT * FROM wins_count;")
    standings = [(row[0], row[1], row[2], row[3]) for row in res]   
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    queryToDatabase("INSERT INTO Matches (player1, player2, winner) VALUES (%s, %s, %s);", 
                    (bleach.clean(winner), bleach.clean(loser), bleach.clean(winner), ))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    res = queryToDatabase("SELECT * FROM wins_count;")
    standings = [(row[0], row[1], row[2], row[3]) for row in res]
    
    pairings = []
    for i in range(0, len(standings), 2):
        pairings.append((standings[i][0], standings[i][1], standings[i + 1][0], standings[i + 1][1]))
    
    return pairings
