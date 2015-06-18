#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def manipulateDB(statement, *args, **kwargs):
    """Manipulates the tournament database.

    Connects and then creates a Cursor object and calls its
    execute() method to perform SQL commands.

    Args:
      statement: a prepared statement to be executed (either a query or insert).
      (optional)fetch: the method fetches one or all remaining rows of a
         query result set and returns a list of tuples.
      (optional)tplValues: provides a tuple of values as the second argument
         to the cursors execute() method to prevent SQL injection.
    """
    fetch = kwargs.get('fetch')
    tplValues = kwargs.get('values')
    results = ''
    conn = connect()
    c = conn.cursor()
    c.execute(statement, tplValues)
    if fetch == "fetchone":
        results = c.fetchone()
    if fetch == "fetchall":
        results = c.fetchall()
    conn.commit()
    conn.close()
    return results


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    query = "TRUNCATE TABLE Matches CASCADE;"
    manipulateDB(query)


def deletePlayers():
    """Remove all the player records from the database."""
    query = "TRUNCATE TABLE Players CASCADE;"
    manipulateDB(query)


def countPlayers():
    """Returns the number of players currently registered."""
    query = "SELECT COUNT(Players.id) FROM Players;"
    count = manipulateDB(query, fetch="fetchone")
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    is handled by my SQL database schema, not in my Python code.)

    Args:
      name: the player's full name (not unique).
    """
    insert = "INSERT INTO Players (name) VALUES(%s);"
    manipulateDB(insert, values=(name,))


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
    return manipulateDB(query, fetch="fetchall")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    insert = "INSERT INTO Matches (winner_id, loser_id) VALUES(%s, %s);"
    manipulateDB(insert, values=(winner, loser,))


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
    results = manipulateDB(query, fetch="fetchall")
    pairings = []
    # Append pairs of players going down the list of v_standings.
    # Player at the top will be paired with player directly below in standings,
    # until there are no more pairs.
    for i in range(0, len(results) - 1, 2):
        pairings.append(results[i] + results[i + 1])

    return pairings
