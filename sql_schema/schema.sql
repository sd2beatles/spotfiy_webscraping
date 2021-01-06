DROP TABLE IF EXISTS artists,top_tracks,audio_features;
CREATE TABLE artists (
  artist_id VARCHAR(255),
  name VARCHAR(255),
  genres VARCHAR(255),
  followers INT UNSIGNED ,
  popularity INT UNSIGNED,
  PRIMARY KEY(artist_id)) ENGINE=InnoDB DEFAULT CHARSET='utf8';

CREATE TABLE top_tracks (
artist_id VARCHAR(255),
track_id VARCHAR(255) ,
track_name VARCHAR(255)  ,
track_popularity INT UNSIGNED ,
PRIMARY KEY(track_id),
FOREIGN KEY(artist_id) REFERENCES artists(artist_id)) ENGINE=InnoDB DEFAULT CHARSET='utf8';

CREATE TABLE audio_features(
track_id VARCHAR(255),
danceability FLOAT ,
energy FLOAT ,
track_key INTEGER ,
loudness FLOAT ,
mode INTEGER ,
speechiness FLOAT ,
acousticness FLOAT ,
instrumentalness FLOAT,
liveness FLOAT,
valence FLOAT,
tempo FLOAT,
PRIMARY KEY(track_id),
FOREIGN KEY(track_id) REFERENCES top_tracks(track_id))ENGINE=InnoDB DEFAULT CHARSET='utf8';
