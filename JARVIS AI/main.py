import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    now = datetime.datetime.now()
    hour = now.hour
    if 0 <= hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"

    day = now.strftime("%A")            
    date_str = now.strftime("%d %B %Y") 
    speak(f"{greet} Today is {day}, {date_str}.")
    speak("I am Jarvis, sir. Please tell me how may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"

    return query

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand()
        if query == "None":
            continue
        query = query.lower()

        # --------------------------
        # Exit / stop commands
        # --------------------------
        if any(word in query for word in ("exit", "bye", "quit", "stop")):
            speak("Goodbye sir. I am going to sleep now. Call me when you need me.")
            break
            
        if any(word in query for word in ("good","good work")):
            speak("thanks sir")

        # --------------------------
        # Wikipedia 
        # --------------------------
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            search_term = query.replace("wikipedia", "").strip()
            if not search_term:
                speak("Please tell me what you want me to search on Wikipedia.")
                continue
            try:
                results = wikipedia.summary(search_term, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("The query is ambiguous. Please be more specific.")
                print("DisambiguationError:", e)
            except Exception as e:
                speak("Sorry, I couldn't fetch the Wikipedia results.")
                print("Wikipedia error:", e)

        # --------------------------
        # Open websites
        # --------------------------
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open notion' in query:
            webbrowser.open("https://www.notion.com")
        elif 'open github' in query:
            webbrowser.open("https://github.com")

        # --------------------------
        # Play music 
        # --------------------------
        elif 'play music' in query or 'play song' in query:
            music_dir = r'D:\Entertainment\songs'   
            if not os.path.exists(music_dir):
                speak("Music folder not found. Please check the music directory path.")
                continue

            songs = [f for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
            if not songs:
                speak("No songs found in the music folder.")
                continue

            song = random.choice(songs)
            speak(f"Playing {song}")
            print(f"Playing: {song}")
            try:
                os.startfile(os.path.join(music_dir, song))
            except Exception as e:
                speak("Sorry, I couldn't play the song.")
                print("Play error:", e)

        # --------------------------
        # Time and open code
        # --------------------------
        elif 'the time' in query or 'what time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strtime}")
            print(f"Sir, the time is {strtime}")

        elif 'open code' in query or 'open vs code' in query:
            codePath = r'C:\Users\Lenovo\AppData\Local\Programs\Microsoft VS Code\Code.exe' 
            if os.path.exists(codePath):
                os.startfile(codePath)
            else:
                speak("VS Code executable not found. Please check the path.")
        
        # --------------------------
                # Notes Feature
        # --------------------------
        elif 'remember that' in query:
            note = query.replace("remember that", "").strip()
            if note:
                with open("notes.txt", "a", encoding="utf-8") as f:
                    f.write(note + "\n")
                speak("I will remember that.")
            else:
                speak("Please tell me what to remember.")

        elif 'what do you remember' in query or 'do you remember anything' in query:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r", encoding="utf-8") as f:
                    notes = f.read().strip()
                if notes:
                    speak("Here are the things I remember.")
                    print(notes)
                    speak(notes)
                else:
                    speak("I don’t have anything remembered yet.")
            else:
                speak("I don’t have any notes saved yet.")
                
                
        # --------------------------
        # Search on Google / YouTube
        # --------------------------
        elif 'search on google' in query:
            search_term = query.replace("search on google", "").strip()
            if search_term:
                speak(f"Searching Google for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                speak("Please tell me what you want me to search on Google.")

        elif 'search on youtube' in query:
            search_term = query.replace("search on youtube", "").strip()
            if search_term:
                speak(f"Searching YouTube for {search_term}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
            else:
                speak("Please tell me what you want me to search on YouTube.")
                
                # --------------------------
        # System Control Commands
        # --------------------------
        elif 'lock' in query:
            speak("Locking the system.")
            os.system("rundll32.exe user32.dll,LockWorkStation")  # locks Windows

        elif 'sleep' in query or 'hibernate' in query:
            speak("Putting the system to sleep.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # sleep/hibernate
        
                # --------------------------
        # Volume Control (Python)
        # --------------------------
        elif 'mute' in query:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(1, None)
            speak("System volume muted.")

        elif 'unmute' in query:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMute(0, None)
            speak("System volume unmuted.")

        elif 'volume up' in query or 'increase volume' in query:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)
            speak("Volume increased.")

        elif 'volume down' in query or 'decrease volume' in query:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMasterVolumeLevelScalar(max(volume.GetMasterVolumeLevelScalar() - 0.1, 0.0), None)
            speak("Volume decreased.")

