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

    def get_token(self):
        header=get_header(self.client_id,self.client_secret)
        payload={"grant_type":"client_credentials"}
        endpoint="https://accounts.spotify.com/api/token"
        raw=requests.post(endpoint,headers=header,data=payload)
        return raw.json()['access_token']

    def search_artists(self):
        token=self.get_token()
        endpoint="https://api.spotify.com/v1/search"
        header={"Authorization":"Bearer {}".format(token)}
        df_artists=pd.DataFrame(columns=['id','name','followers','popularity','genres'])
        for index,artist in enumerate(self.artists):
            params={'q':artist,
                    'type':'artist',
                    'limit':'1'}
            r=requests.get(endpoint,params=params,headers=header)
            if r.status_code==400:
                print("check out your syntax carefully!")
            elif r.status_code==409:
                retry=json.loads(r.headers)['Retry-After']
                time.sleep(int(retry))
                r=requests.get(endpoint,params=params,headers=header)
            raw=r.json()['artists']['items'][0]
            if type(raw['genres'])==list:
                genre=str(raw['genres'])
            else:
                genre=raw['genres']
            record=(raw['id'],raw['name'],raw['followers']['total'],raw['popularity'],genre)
            df_artists.loc[index]=record
        return df_artists






def main():
    client_id="161975af6e9c43eaa63de06b51331fdb"
    client_secret="5b081f7826084b10824544dd8d439911"
    result=Spotify(client_id,client_secret,['BTS'])
    df=result.search_artists()
    print(df)


if __name__ == '__main__':
    main()
