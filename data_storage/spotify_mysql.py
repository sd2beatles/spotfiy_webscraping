
import  sys
import logging
import requests
import json
import base64
import time
import pymysql
from datetime import datetime




def get_header(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode("utf-8")).decode("ascii")
    header={"Authorization":"Basic {}".format(encoded)}
    return header


class Spotify(object):
    def __init__(self,client_id,client_secret,artists):
        self.client_id=client_id
        self.client_secret=client_secret
        unique_artists=set(artists)
        if len(artists)==len(unique_artists):
            self.artists=artists
        else:
            self.artists=artists
        self.artists_info=dict()
        self.track_ids=list()



    def get_header(self):
        header=get_header(self.client_id,self.client_secret)
        payload={"grant_type":"client_credentials"}
        endpoint="https://accounts.spotify.com/api/token"
        raw=requests.post(endpoint,headers=header,data=payload)
        token=json.loads(raw.text)['access_token']
        return {"Authorization":"Bearer {}".format(token)}

    def insert_row(self,cursor,info,table):
        assert type(info)==dict,"the input type must be dictionary"
        cols=','.join(info.keys())
        placeholder=','.join(['%s']*len(info))
        key_placeholder=','.join(["{0}=%s".format(col) for col in info.keys()])
        query="INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" %(table,cols,placeholder,key_placeholder)
        cursor.execute(query,list(info.values())*2)


    def set_artists_id(self):
        header=self.get_header()
        endpoint="https://api.spotify.com/v1/search"
        for artist in self.artists:
            params={
            'q':artist,
            'type':'artist',
            'limit':1
            }
            r=requests.get(endpoint,params=params,headers=header)
            raw=json.loads(r.text)['artists']['items'][0]
            self.artists_info[artist]=raw['id']



    def artist_search(self,artist,header):
        endpoint="https://api.spotify.com/v1/search"
        params={
        'q':artist,
        'type':'artist',
        'limit':1
        }
        r=requests.get(endpoint,params=params,headers=header)
        raw=json.loads(r.text)['artists']['items'][0]

        info={
        'artist_id':raw['id'],
        'name':raw['name'],
        'genres':raw['genres'],
        'followers':raw['followers']['total'],
        'popularity':raw['popularity']}

        if type(raw['genres'])==list:
            info.update({'genres':str(raw['genres'])})
        return info



    def set_artists(self,cursor):
        endpoint="https://api.spotify.com/v1/search"
        header=self.get_header()

        for artist in self.artists:
            try:
                info=self.artist_search(artist,header)
                self.artists_info[info['name']]=info['artist_id']
                self.insert_row(cursor,info,'artists')
            except:
                msn="Somehting unexcpted issue has arisen when searching infomration on {}".format(info['name'])
                print(msn)
                continue
        now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('The function,set_artists, has been successfully finshed its task on {}'.format(now))







    def search_tracks(self,artist_id,cursor):
         info_lists=list()
         endpoint="https://api.spotify.com/v1/artists/{}/top-tracks".format(artist_id)
         header=self.get_header()
         params={'country':'US'}
         r=requests.get(endpoint,params=params,headers=header)
         tracks=json.loads(r.text)['tracks']
         for i in range(len(tracks)):
             info={
             'artist_id':artist_id,
             'track_id':tracks[i]['id'],
             'track_name':tracks[i]['name'],
             'track_popularity':tracks[i]['popularity']}
             self.track_ids.append(info['track_id'])
             self.insert_row(cursor,info,'top_tracks')


    def set_tracks(self,cursor):
        if not self.artists_info:
            self.set_artists_id()
            print("artis information has been successfully stored.")

        for artist_id in self.artists_info.values():
            self.search_tracks(artist_id,cursor)

        now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('The function,set_tracks, has been successfully finshed its task on {}'.format(now))


    def set_audio_features(self,cursor):
        if not self.track_ids:
            logging.error("Run set_tracks function before proceeding to the next")
            sys.exit(1)

        endpoint="https://api.spotify.com/v1/audio-features"
        header=self.get_header()
        cols_removed=['type','uri','track_href','analysis_url','duration_ms','time_signature']
        for index in range(0,len(self.track_ids),100):
            params={'ids':','.join(self.track_ids[0:index+100])}
            r=requests.get(endpoint,headers=header,params=params)
            info=dict()
            for feature in json.loads(r.text)['audio_features']:
                info.update({col:value for col,value in feature.items() if col not in cols_removed})
                info['track_key']=info.pop('key')
                info['track_id']=info.pop('id')
                self.insert_row(cursor,info,'audio_features')
        now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('The function,set_audio_features,has been successfully finshed its task on {}'.format(now))







def main():
    client_id="161975af6e9c43eaa63de06b51331fdb"
    client_secret="9ad11c884ae14fd0ae95ce501d7be190"
    artists=["BTS","Taylor Swift"]
    #create an instance of Spotify class
    spotify=Spotify(client_id,client_secret,artists)


    #set up an environment for sql databases
    host="spotify.c6jgvnsrw5a1.us-east-1.rds.amazonaws.com"
    port=3306
    username="david"
    database="spotify"
    password="navercom123"


    conn=pymysql.connect(host,user=username,passwd=password,db=database,port=port,use_unicode=True,charset="utf8")
    cursor=conn.cursor()
    try:
        conn=pymysql.connect(host,user=username,passwd=password,db=database,port=port,use_unicode=True,charset='utf8')
        cursor=conn.cursor()
    except:
        logging.error("Connection to RDS has failed!")

    spotify.set_artists(cursor)
    spotify.set_tracks(cursor)
    spotify.set_audio_features(cursor)
    conn.commit()



if __name__=='__main__':
    main()
