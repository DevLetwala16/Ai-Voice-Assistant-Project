# Libraries Include....
import speech_recognition as sr
import webbrowser as web
import pyttsx3  # for a text to speech convert
import pocketsphinx
import MusicLibrary as ml
import requests
import winsound

# import pywhatkit  # for easy searching
import Soical_media_Library as sml
import wikipedia as wp
import cgi
from googletrans import Translator

######################################### Upcomming Update Features #########################################
# gTTs google cloud text to speech convertor --->  11 labs ----> pyttsx3 change a voice...  ---->
# free api for a other tooles --->background voices ---> googlr assistante ----> stop or sleeps...
# Sleep and stop assistant Features ( wip Work )
#############################################################################################################
api_key = "pub_56198f1a60df4611a52b00182d18872a"  ###### API Id For fatch news
url_en = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=in&language=en"
url_hi = f"https://newsdata.io/api/1/latest?apikey={api_key}&country=in&language=hi"

######################### Working of Text To Speech Convert ####################################
################################################################################################
## For Information !!!
# import pyttsx3
# engine = pyttsx3. init()
# engine.say("I will speak this text")
# engine.runAndWait()
################################################################################################


# Functions For Work...


# 1. Functions For speak somthing...
def speak(text, command):
    engine = pyttsx3.init()
    engine.setProperty("rate", 200)  # Speed controll
    engine.setProperty("volume", 1)  # Volume range(0 to 1)
    voices = engine.getProperty("voices")
    engine.setProperty(
        "voice", voices[9].id if "hindi" in command.lower() else voices[3].id
    )  # (3),4,6,8,(9) Voices id
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    return


# 2.  Functions For Task...
def processcommand(command):
    sucess = False
    # social Media and other important................
    if "open" in command.lower():
        list_1 = command.lower().replace("open", "").strip()
        for key, value in sml.website.items():
            if key in list_1:
                sucess = True
                web.open(value)
                winsound.PlaySound("1.wav", winsound.SND_FILENAME)
                break

        if not (sucess):
            web.open(f"https://www.google.com/search?q={command}?")
            winsound.PlaySound("1.wav", winsound.SND_FILENAME)

    # song Search If it is avilable in library so Diretly Use This other Wise search on Yotube....
    elif "song" in command.lower() or "play" in command.lower():

        list_m1 = command.lower().replace("song", "").replace("play", "").strip()
        for key, value in ml.music.items():
            if key in list_m1:
                sucess = True
                web.open(value)
                winsound.PlaySound("1.wav", winsound.SND_FILENAME)
                break

        if not (sucess):
            final_command = command.lower().replace(" ", "+")
            web.open(f"https://www.youtube.com/results?search_query={final_command}")
            winsound.PlaySound("1.wav", winsound.SND_FILENAME)

    # teling news in English.....
    elif "news" in command.lower() and not ("hindi" in command.lower()):
        # For English News
        response = requests.get(url_en)
        if response.status_code == 200:
            data = response.json()
            for article in data.get("results", []):
                speak(article["title"], command)

            winsound.PlaySound("1.wav", winsound.SND_FILENAME)

    # teling news in hindi.....
    elif "news" in command.lower() and "hindi" in command.lower():
        # For Hindi News
        response = requests.get(url_hi)
        if response.status_code == 200:
            data = response.json()
            for article in data.get("results", []):
                speak(article["title"], command)

            winsound.PlaySound("1.wav", winsound.SND_FILENAME)

    # For Wikipedia Search Like Some information about Some Famouse...

    elif (
        any(
            word in command.lower() for word in ["who is", "what is", "where is"]
        )  ## new syntex
        and "time" not in command.lower()
    ):
        topic = (
            command.lower()
            .replace("who", "")
            .replace("where", "")
            .replace("what", "")
            .replace("is", "")
            .replace("in hindi", "")
            .strip()
        )

        Answer = wp.summary(topic, sentences=5, auto_suggest=False)

        if "hindi" in command.lower():
            try:
                wp.set_lang("hi")
                translator = Translator()
                hindi_translation = translator.translate(Answer, dest="hi")
                hindi_text = hindi_translation.text
                speak(Answer, "hindi")
            except:
                print("Not Avilable in Hindi !!! ")
                speak("Not Avilable in Hindi !!! ")
        else:
            wp.set_lang("en")
            speak(Answer, "")
            winsound.PlaySound("1.wav", winsound.SND_FILENAME)

    else:
        # This opens a browser with the search results by Default....
        web.open(f"https://www.google.com/search?q={command}?")
        winsound.PlaySound("1.wav", winsound.SND_FILENAME)


# Main Program...
if __name__ == "__main__":

    winsound.PlaySound("1.wav", winsound.SND_FILENAME)
    speak("Initialization Mummy Powered by Softcapphyjas !!!", "")

    while True:
        # when we call Josoft ( Mummy )  Then Ai Asistant active....
        try:
            # recognize speech using google
            # obtain audio from the microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.75)
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            print("Recognization...")
            call = r.recognize_google(audio)
            if "mummy" in call.lower():
                winsound.PlaySound("1.wav", winsound.SND_FILENAME)
                print("Mummy Active !!!")
                speak("Ha dikara !!!", "")
                # listening Command...
                print("Listening...")

                with sr.Microphone() as source:
                    audio = r.listen(source)

                print("Recognization...")
                winsound.PlaySound("3.wav", winsound.SND_FILENAME)
                command = r.recognize_google(audio)
                print(command)
                processcommand(command)

        except Exception as e:  # error Phase !!!
            print("Mummy Could Not Understand Audio !!! ")
