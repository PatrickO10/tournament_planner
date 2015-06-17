#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query = "TRUNCATE TABLE matches CASCADE;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    query = "TRUNCATE TABLE players CASCADE;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(Players.id) FROM Players;")
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    insert = "INSERT INTO Players (name) VALUES(%s);"
    conn = connect()
    c = conn.cursor()
    c.execute(insert, (name,))
    conn.commit()
    conn.close()

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
    query = "SELECT * FROM v_standings;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    insert = "INSERT INTO Matches (winner_id, loser_id) VALUES(%s, %s);"
    conn = connect()
    c = conn.cursor()
    c.execute(insert, (winner, loser))
    conn.commit()
    conn.close()


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
    query = "SELECT v_standings.id, v_standings.name FROM v_standings;"
    conn = connect()
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    pairings = []
    # Append pairs of players going down the list of v_standings.
    # Player at the top will be paired with player directly below in standings.
    for i in range(0, len(results) - 1, 2):
        pairings.append(results[i] + results[i + 1])
    conn.close()
    return pairings
