import sys
import logging
import requests
import json
import pandas as pd
import base64
import time

def get_header(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode("utf-8")).decode("ascii")
    header={"Authorization":"Basic {}".format(encoded)}
    return header

def errorMessage(r):
    if r.status_code==400:
        print("check out your syntax carefully!Try it again")
        sys.exit(1)
    elif r.status_code==409:
        retry=json.loads(r.headers)['Retry-After']
        time.sleep(int(retry))
        r=requests.get(endpoint,params=params,headers=header)
        return r
    elif r.status_code==200:
        return r



class Spotify(object):
    def __init__(self,client_id,client_secret,artists):
        self.client_id=client_id
        self.client_secret=client_secret
        unique_artist=set(artists)
        if artists is not None:
            if len(artists)==len(unique_artist):
                self.artists=artists
            else:
                self.artists=unique_artist
        else:
            logging.error("No artist is found!")
            sys.exit(1)
        self.artists_dict=None


    def get_token(self):
        header=get_header(self.client_id,self.client_secret)
        payload={"grant_type":"client_credentials"}
        endpoint="https://accounts.spotify.com/api/token"
        raw=requests.post(endpoint,headers=header,data=payload)
        return raw.json()['access_token']


    def artist_top_tracks(self,artist_id):
        endpoint="https://api.spotify.com/v1/artists/{}/top-tracks".format(artist_id)
        token=self.get_token()
        header={"Authorization":"Bearer {}".format(token)}
        params={'country':'US'}
        raw=requests.get(endpoint,headers=header,params=params)
        r=errorMessage(raw)

        tracks=r.json()['tracks']
        records=list()
        for i in range(len(tracks)):
            record=[artist_id,tracks[i]['id'],tracks[i]['name'],tracks[i]['popularity']]
            records.append(record)
        return records

    def artist_search(self,artist,header):
        endpoint=endpoint="https://api.spotify.com/v1/search"
        params={'q':artist,
                'type':'artist',
                'limit':'1'}
        r=requests.get(endpoint,params=params,headers=header)
        respon=errorMessage(r)
        return respon

    def get_tracks(self):
        artists=dict()
        token=self.get_token()
        header={"Authorization":"Bearer {}".format(token)}
        if not self.artists_dict:
            for artist in self.artists:
                respon=self.artist_search(artist,header)
                raw=respon.json()['artists']['items'][0]['id']
                artists[artist]=raw
            self.artists_dict=artists
        #delete dicts for preventing the waste of memeory
        del artists
        #start colleting data
        records=list()
        for artist in self.artists:
            artist_id=self.artists_dict[artist]
            record=self.artist_top_tracks(artist_id)
            records+=record
        collected=pd.DataFrame(records,columns=["artist_id","track_id","track_name","tack_popularity"])
        return collected


    def get_artists(self):
        token=self.get_token()
        endpoint="https://api.spotify.com/v1/search"
        header={"Authorization":"Bearer {}".format(token)}
        df_artists=pd.DataFrame(columns=['id','name','followers','popularity','genres'])
        for index,artist in enumerate(self.artists):
            respon=self.artist_search(artist,header)
            raw=respon.json()['artists']['items'][0]
            if type(raw['genres'])==list:
                genre=str(raw['genres'])
            else:
                genre=raw['genres']
            record=(raw['id'],raw['name'],raw['followers']['total'],raw['popularity'],genre)
            df_artists.loc[index]=record
        df_artists,df_genres=self.relation_divisor(df_artists)
        if not  self.artists_dict:
            self.artists_dict={name:s_id for s_id,name in zip(df_artists['id'],df_artists['name'])}
        return df_artists,df_genres

    def relation_divisor(self,data):
        assert type(data) is pd.DataFrame
        dif_cols=['id','genres']
        cols=data.columns.values.tolist()
        cols.remove("genres")
        return data.loc[:,cols],data.loc[:,dif_cols]







def main():
    client_id="161975af6e9c43eaa63de06b51331fdb"
    client_secret="5b081f7826084b10824544dd8d439911"
    #"BTS","Taylor Swift","The Weeknd","Christine and the Queens","Bob Dylan","Cardi B feat. Megan Thee Stallion"
    #result=Spotify(client_id,client_secret,["BTS","Dua Lipa","The Weeknd","Christine and the Queens","Bob Dylan","Cardi B"])
    a=Spotify(client_id,client_secret,['BTS',"Dua Lipa"])


if __name__ == '__main__':
    main()
