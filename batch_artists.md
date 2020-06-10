```python
def get_token(client_id,client_secret):
    encoded=base64.b64encode("{}:{}".format(client_id,client_secret).encode('utf-8')).decode('ascii')
    header={'Authorization':'Basic {}'.format(encoded)}
    payload={'grant_type':'client_credentials'}
    url=' https://accounts.spotify.com/api/token'
    r=requests.post(url,headers=header,data=payload)
    raw={'Authorization':'Bearer {}'.format(r.json()['access_token'])}
    return raw
    
      
def main():
    try:
        conn=pymysql.connect(host='localhost',user='root',db='production',passwd='1234',port=3306,charset='utf8')
        cursor=conn.cursor()
    except:
        logging.error('can not acess the db')
        sys.exit(1)
    conn.commit()
    cursor.execute('select id from artists')
    artists=list()
    for id, in cursor.fetchall():
        artists.append(id)
    artists_batch=[artists[i:i+50] for i in range(0,len(artists),50)]
    headers=get_token(client_id,client_secret)
    
    for i in artists_batch:
        ids=','.join(i)
        url="https://api.spotify.com/v1/artists?ids={}".format(ids)
        headers=get_token(client_id,client_secret)
        r=requests.get(url,headers=headers)
        raw=json.loads(r.text)
        print(raw)
        
   
          
if __name__=='__main__':
    main()
```
