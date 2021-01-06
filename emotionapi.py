import requests
import json
import lyricapi

def get_emotions(spot_id):
    
    text = lyricapi.get_lyrics(spot_id)
 
    api_key = "zPjjWsESahr9XmEodCVXJ2A9AwEBgRnj0ggAR5d6FO8"

    response = requests.post("https://apis.paralleldots.com/v4/emotion", data={ "api_key": api_key, "text":text})
    
    if "code" in response.json() and response.json()["code"]==403:
        return "Daily Limit Exceeded."

    return response.json()['emotion']
