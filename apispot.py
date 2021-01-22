import requests
import json
import os

def get_tracks(spot_id):
          
    payload = {"grant_type":"client_credentials"}
    header = {"Authorization":os.getenv("SPOTIFY_TOKEN")}

    r = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=header)

    token = r.json()["access_token"]

    playlist_id = spot_id
    
    url = 'https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks'
    p = 'Bearer '+ token
    header2 = {"Authorization":p}
    
    query = {"fields":"total,items"}
    o = []
    l = requests.get(url,headers=header2,params=query)
    o.append(l.json())
    track_count = o[0]["total"]
    #print(track_count)
    
    if track_count > 100:     
        offnum = int((track_count - 100)/100)+1
        
        for i in range(1,offnum+1):
            offt = str(i*100)
            query = {"fields":"total,items","offset":offt}
            l = requests.get(url,headers=header2,params=query)
            o.append(l.json())
    
    #print(len(o))
            

    tracks_list = []
    for h in range(0,len(o)):

        for i in range(0,len(o[h]["items"])):
            tracks_list.append([o[h]["items"][i]["track"]["name"],o[h]["items"][i]["track"]["album"]["artists"][0]["name"]])
        
    #print(len(tracks_list),tracks_list)
    
    #with open ('tracks.txt','w',encoding="utf-8") as file:
        #file.write(str(tracks_list))
        
    return tracks_list
            

