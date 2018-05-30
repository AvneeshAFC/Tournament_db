-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Reference - https://discussions.udacity.com/search?q=database%20tournament

drop database if exists tournament;
-- drops the previous database for running multiple times

create database tournament;
-- create a databse named tournament

\c tournament;
-- connecting to the tournament database

create table players (id serial primary key, player_name text);
--players table with id as the primary key

create table matches (game_id serial primary key,
                      won integer references players(id),
                      loss integer references players(id));
-- matches table with game_id as the primary key and win/loss referencing to
-- id of players table

create view mwins as select players.id, players.player_name,
count(matches.won) as wins from matches right join players on
matches.won=players.id group by players.id order by wins desc;
-- a view to extract games won by respective players

create view mloss as select players.id, players.player_name,
count(matches.loss) as losses from matches right join players on
matches.loss=players.id group by players.id order by losses;
-- a view to extract games lost by respective players

create view standing as select mwins.id, mwins.player_name, mwins.wins,
mloss.losses + mwins.wins as games, mloss.losses from mwins, mloss where
mwins.id=mloss.id order by mwins.wins desc;
-- a view to extract the player standings based on the number of games
-- won by the players respectively in descending order