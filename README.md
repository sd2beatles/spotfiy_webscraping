# Spotify Web Scrapper
Spotify Web scraper crawls throuhg the Spotify web interface and extracts a variety of information on artists of your interest

## 1) System Environments

- python 3.8
- mysql 5.7

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
#CREATE TABLES 
USE PRODUCTION
CREATE TABLE artists (artist_id VARCHAR(255),name VARCHAR(255),followers INTEGER,popularity INTEGER,PRIMARY KEY(id)) ENGINE=InnoDB DEFAULT CHARSET='utf8';
CREATE TABLE top_trakcs (artist_id VARCHAR(255),track_id VARCHAR(255),track_name VARCHAR(255),track_popularity INTEGER,PRIMARY KEY(track_id)) ENGINE=InnoDB DEFAULT CHARSET='utf8';

CREATE TABLE audio_features (danceability FLOAT,energy FLOAT,key INTEGER,loundness FLOAT,mode INTEGER,speechiness FLOAT,acousticness FLOAT,instrumentalness FLOAT,valence FLOAT,tempo FLOAT,id VARCHAR(255) 


```

