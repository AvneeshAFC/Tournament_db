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
    db=connect()
    a=db.cursor()
    a.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db=connect()
    a=db.cursor()
    a.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db=connect()
    a=db.cursor()
    a.execute("select count(*) as num from players;")
    count=a.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db=connect()
    a=db.cursor()
    a.execute("insert into players (player_name) values (%s)",(name,))
    db.commit()
    db.close()


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
    db=connect()
    a=db.cursor()
    a.execute("select id, player_name, wins, games from standing;")
    st=a.fetchall()
    db.close()
    return st


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db=connect()
    a=db.cursor()
    a.execute("insert into matches (won, loss) values (%s, %s)",(winner,loser))
    db.commit()
    db.close()


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
    std=playerStandings()   #Gets the standings from the function above
    num=int(countPlayers())     #Gets the no. of players participating
    pairings=[]     # initialize pairings
    if (num>0):
        for x in range(num):
            if (x%2==0):
                id1 = std[x][0]
                name1  = std[x+1][0]
                id2 = std[x+1][0]
                name2 = std[x+1][1]
                pair = (id1,name1,id2,name2)    # makes parings of 2 players
                pairings.append(pair)   # appends the pair into the pairings
    return pairings


