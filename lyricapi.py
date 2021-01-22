import requests
import json
import apispot
import os

def get_lyrics(spot_id):

    tracks = apispot.get_tracks(str(spot_id))
    key = os.getenv("MUSIXMATCH_TOKEN")
    all_lyrics = ""
    c = 0

    for track in tracks:
        c+=1
        par1 = {"apikey":key,"q_track":"","q_artist":"","f_has_lyrics":1}
        par1["q_track"] = track[0]
        par1["q_artist"] = track[1]

        r1 = requests.get("https://api.musixmatch.com/ws/1.1/track.search",params=par1)
    
        if r1.json()["message"]["header"]["available"] != 0 or r1.json()["message"]["header"]["status_code"] != 200:
        
            num = r1.json()["message"]["body"]["track_list"][0]["track"]["track_id"]

            par2 = {"apikey":key, "track_id":str(num)}

            r2 = requests.get("https://api.musixmatch.com/ws/1.1/track.lyrics.get",params=par2)


            lyric_raw = r2.json()["message"]["body"]["lyrics"]["lyrics_body"]
            lyric = lyric_raw.replace("\n"," ")
            ind = lyric.find("...")
            lyric = lyric[:ind-1]
    
            all_lyrics += lyric
    
    return all_lyrics
