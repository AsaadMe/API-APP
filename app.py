from flask import Flask , request, render_template
from flask_sqlalchemy import SQLAlchemy
import sys
import emotionapi
import apispot
import lyricapi
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.String())
    emotions = db.Column(db.String())
    
    
    def __init__(self, playlist_id, emotions):
        self.playlist_id = playlist_id
        self.emotions = emotions

@app.route('/', methods=['GET','POST'])
def index():
    init = '0'
    if request.method == 'POST':
        spotid = request.form['text']
        em = emotionapi.get_emotions(spotid)
        
        if em == "Daily Limit Exceeded.":
            return em
        
        else:
        
            happy='{:.2f}'.format(em['Happy']*100)
            sad='{:.2f}'.format(em['Sad']*100)
            angry='{:.2f}'.format(em['Angry']*100)
            fear='{:.2f}'.format(em['Fear']*100)
            excited='{:.2f}'.format(em['Excited']*100)
            bored='{:.2f}'.format(em['Bored']*100)
            
            data = Result(playlist_id=str(spotid) , emotions=str(em) )
            db.session.add(data)
            db.session.commit()

            return render_template('index.html',happy=happy , sad=sad , angry=angry , fear=fear , excited=excited , bored=bored)
    return render_template('index.html',happy=init , sad=init , angry=init , fear=init , excited=init , bored=init)
    
@app.route('/api-tracks/', methods=['GET'])
def get_tracklist():
    
    spotid = request.args.get("spotid", None)
    tracks = apispot.get_tracks(spotid)
    par = ""
    for track in tracks:
        par += "<p>"+track[0]+" - "+track[1]+"</p>"
    return par
    
@app.route('/api-lyrics/', methods=['GET'])
def get_lyricsstr():
    
    spotid = request.args.get("spotid", None)
    lyrics = lyricapi.get_lyrics(spotid)
    
    return lyrics
 
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
