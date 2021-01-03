# Spotify Web Scrapper
Spotify Web scraper crawls throuhg the Spotify web interface and extracts a variety of information on artists of your interest

## 1) System Environments

- python 3.8
- mysql 8.0

After obtaining all relevanat infomration of artists from the site, we can save it to the seleceted table in database.

## 2) Flow Chart For The Designed Database 

![image](https://user-images.githubusercontent.com/53164959/83850098-5cd3ed80-a74b-11ea-821a-e712eed20ee0.png)


## 3) Brief Explnation For Codes

>- Individual Search : Get Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a keyword
>                      string
>- Batch Search :  Get Spotify catalog information for several artists based on their Spotify IDs
                  (Be aware that the manimum number for each run is 50 IDs)


### 4) mysql aws

```linux
mysql -h <endpoint> -p <port_number> -u <master_name> -p 
```

```mysql
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




```

