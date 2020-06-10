
```python
client_id='replace here'
cliente_secret='replace_here'

def get_header(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    header={'Authorization':'Basic {}'.format(encoded)}
    return header

class spotfiySearch(object):
    def __init__(self,client_id,client_secret,artists,cursor):
        self.client_id=client_id
        self.client_secret=client_secret
        self.cursor=cursor
        #to prevent searching for duplicate artists
        if artists!=None:
            unique_artists=set(artists)
            if len(artists)==len(unique_artists):
                self.artists=artists
            else:
                self.artists=unique_artists
        else:
            logging.error('No artist is found')
            sys.exit(1)
        self.cursor=cursor
    
    def get_accessToken(self):
        url=url=' https://accounts.spotify.com/api/token'
        header=get_header(self.client_id,self.client_secret)
        data={'grant_type':'client_credentials'}
        t=requests.post(url,headers=header,data=data)
        token=t.json()['access_token']
        return token
    
    def search_save(self,tableName):
       access_token=self.get_accessToken()
       headers={'Authorization':'Bearer {}'.format(access_token)}
       for a in self.artists:
        params={
            'q':a,
            'type':'artist',
            'limit':'1'}
        r=requests.get("https://api.spotify.com/v1/search",params=params,
                        headers=headers)
        if r.status_code==429:
            retry=json.loads(r.headers)['Retry-After']
            time.sleep(int(retry))
            r=requests.get("https://api.spotify.com/v1/search",params=params,
                        headers=params)
        elif r.status_code==401:
            headers=get_header(self.client_id,self.client_secrets)
            r=requests.get("https://api.spotify.com/v1/search",params=params,headers=headers)
        raw=r.json()['artists']['items'][0]
        info={
             'id':raw['id'],
             'name':raw['name'],
             'followers':raw['followers']['total'],
             'popularity':raw['popularity'],
             'image_url':raw['images'][0]['url'],
             'genres':raw['genres']
            }
        if type(info['genres'])==list:
            info.update({'genres':str(raw['genres'])})
        
        
        placeholder=','.join(['%s']*len(info))
        columns=','.join(info.keys())
        sql='insert into %s (%s) values (%s)' %(table_name,columns,placeholder)
        self.cursor.execute(sql,list(info.values()))
```
