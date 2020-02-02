from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import requests
import keyboard
#from playsound import playsound

str='a'
def talk(audio):
    print(audio)
    #playsound('audio.mp3')
    for line in audio.splitlines():
        os.system("say " + audio)
    text_to_speech = gTTS(text=audio, lang='en')
    text_to_speech.save('audio1.mp3')
    os.system('mpg123 audio.mp3')


def myCommand(): 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();
    return command


def assistant(command):
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')
    elif 'shutdown my pc' in command:
        os.system("shutdown /s /t 1")
    elif 'open computer' in command:
        keyboard.press_and_release('win+e')
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            if domain=="d drive":
                os.startfile(r"D:")
            elif domain=="e drive":
                os.startfile(r"E:")
            else:
                pass
            print('Done!')
        else:
            pass
        
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'what\'s going on' in command:
        talk('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talk(str(res.json()['joke']))
        else:
            talk('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather_key='2db94bf59f9168b21cec03984c57f083'
            url='https://api.openweathermap.org/data/2.5/weather'
            params={'APPID':weather_key,'q':city,'units':'imperial'}
            response=requests.get(url,params=params)
            weather=response.json()
            q=weather['name']
            z=weather['weather'][0]['description']
            e=weather['main']['temp']
            r=weather['wind']['speed']
            finall='City: %s \nDescription: %s \nTemperature(ͦF): %s \nWind Speed(mph): %s' %(q,z,e,r)
            print(finall)
talk('I am ready for your command')

while True:
    assistant(myCommand())
    