from audio_features import Spotify

def saveFile(records,mode):
    assert mode in ['json','parqeut']
    if mode=="json": 
        with open('audio_features.json','w') as f:
            json.dump(records,f)
        
    elif mode=="parquet":
        tracks=pd.DataFrame(records)
        tracks.to_parquet('audio_features.parquet',engine='pyarrow',compression='snappy')

def main():
    token=getToken(client_id,client_secret)
    artists=["BTS","Taylor Swift"]
    records=[]
    try:
        for artist in artists:
            record=Spotify.getArtistID(artist,1,token).getAudioFeatures()
            records+=record
    except:
        print("The artist,{},is not currently registered to Spotify".format(artist))
    
    saveFile(records,'json')
    with open('audio_features.json','r') as f:
        data=json.loads(f.read())
        print(data)



if __name__=='__main__':
    main()
