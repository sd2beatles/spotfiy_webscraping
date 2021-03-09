from accessToken import *
import requests
import json
import os

class Spotify(object):
    def __init__(self,record,header):
        self.record=record
        self.header=header
        self.features=list()
    
    @classmethod
    def getArtistID(cls,name,limit,header):
        endpoint='https://api.spotify.com/v1/search'
        params={
            'q':name,
            'type':'artist',
            'limit':limit
        }
        raw=requests.get(endpoint,params=params,headers=header)
        r=json.loads(raw.text)['artists']['items'][0]
        keys=['id','name','genres']
        record={key:str(r[key]) for key in keys }
        return  Spotify(record,header)

    def getTracks(self):
        endpoint="https://api.spotify.com/v1/artists/{}/top-tracks".format(self.record['id'])
        params={'country':'US'}
        r=requests.get(endpoint,params=params,headers=self.header)
        tracks=json.loads(r.text)['tracks']
        records=list()
        for i in range(len(tracks)):
            records.append(tracks[i]['id'])
        return records

    def getAudioFeatures(self):
        result=[]
        tracks=','.join(self.getTracks())
        endpoint='https://api.spotify.com/v1/audio-features'
        params={'ids':tracks}
        raw=requests.get(endpoint,params=params,headers=self.header)
        records=json.loads(raw.text)['audio_features']
        ncol=['type','id','uri','track_href','analysis_url']
        for record in records:
            track={k:v for k,v in record.items() if k not in ncol}
            track['genres']=self.record['genres']
            result.append(track)
        return result
