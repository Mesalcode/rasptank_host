import speech_recognition
import pafy
import vlc
import re
import urllib.request
import urllib.parse
import sys
from sultan.api import Sultan
import time
import pyglet
recognizer = speech_recognition.Recognizer()
def say(text):
    pass
def listenForCall():
    with speech_recognition.Microphone() as source:
        print("Waiting for 'Ok Tank'")
        audio = recognizer.listen(source)
        try:
            recognized_speech = recognizer.recognize_google(audio , language='de-DE')
            if ("ok" in recognized_speech or "okay" in recognized_speech or "Kid"):
                listenForCommand()
            else:
                print("Recognized non-consulting phrase: " + recognized_speech)
                listenForCall()

        except:
            listenForCall()
    pass
def listenForCommand():
    with speech_recognition.Microphone() as source:
        print("Listening for voice command")
        audio = recognizer.listen(source)
    
        recognized_speech = recognizer.recognize_google(audio , language='de-DE')
        computeCommand(recognized_speech)
        
        #print("Did not understand the voice command")
        #listenForCall()
def computeCommand(cmd):
    print("Now computing: " + cmd.lower())
    if (cmd.lower().find("spiel")>-1):
        playSong(cmd.lower()[(cmd.lower().find("spiel")+5):])
def listenForListeningCommand(player, volume):
    with speech_recognition.Microphone() as source:
        print("Listening for while listening command")
        try:
            audio = recognizer.listen(source, timeout=3) # the timeout is import, when not setting a timeout, the system tries to figure out words from the music.
            recognized_speech = recognizer.recognize_google(audio , language='de-DE')
            print(recognized_speech)
            if ("stop" in recognized_speech.lower()):
                player.stop()
            elif ("leiser" in recognized_speech.lower()):
                volume-=25
                if (volume >0):
                    player.audio_set_volume(volume)
                else:
                    player.audio_set_volume(0)
            elif ("lauter" in recognized_speech.lower()):
                volume+=25
                player.audio_set_volume(volume)
        except:
            listenForListeningCommand(player, volume)

        
        
def playSong(songTitle):
    print("Now playing:",songTitle)
    #source: https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video
    query_string = urllib.parse.urlencode({"search_query" : (songTitle+" song")})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("First result for songname = http://www.youtube.com/watch?v=" + search_results[0])
    #source: https://stackoverflow.com/questions/49354232/how-to-stream-audio-from-a-youtube-url-in-python-without-download
    url = search_results[0] 
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    print("Found optimal url: " + playurl)
    #player = vlc.MediaPlayer(playurl)
    #player.play()
    #while True:
    #    pass
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    player.set_mrl(playurl, ":no-video")
    #Media = Instance.media_new(playurl)
    #Media.get_mrl()
    #player.set_media(Media)
    volume = 100
    player.play()
    player.audio_set_volume(volume)
    while player.get_state()!= 6 and player.get_state()!=5: #State defininitions = http://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.State-class.html
        listenForListeningCommand(player, volume)
        pass
say("Der Rasptank Sprachserver ist nun online. Ich kann Musik abspielen.")
while True:
    listenForCall()