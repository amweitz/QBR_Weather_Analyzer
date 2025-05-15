-- Create the database
-- NOTE: Run this part outside psql or in a different DB like 'postgres'
CREATE DATABASE qbr;

-- Connect to the new database (only works if run with tools that support \connect)
\connect qbr

-- Create nfl_weather table
CREATE TABLE public.nfl_weather (
    year        INTEGER,
    week        TEXT,
    team        TEXT,
    temperature DOUBLE PRECISION
);

-- Create weekly_qbr table
CREATE TABLE public.weekly_qbr (
    season     INTEGER,
    week_text  TEXT,
    team_abb   TEXT,
    rank       DOUBLE PRECISION,
    qbr_total  DOUBLE PRECISION,
    pts_added  DOUBLE PRECISION,
    qb_plays   DOUBLE PRECISION,
    epa_total  DOUBLE PRECISION,
    pass       DOUBLE PRECISION,
    run        DOUBLE PRECISION,
    exp_sack   DOUBLE PRECISION,
    penalty    DOUBLE PRECISION,
    qbr_raw    DOUBLE PRECISION,
    sack       DOUBLE PRECISION,
    first_name TEXT,
    last_name  TEXT,
    team       TEXT,
    opp_abb    TEXT,
    opp_name   TEXT
);
