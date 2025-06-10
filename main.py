import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library # Assuming this file/module exists and has the 'music' dictionary


# Import your PersonalAIAgent from client.py
from client import PersonalAIAgent

# --- API Key (HARDCODED as requested for now) ---
# IMPORTANT: This is for quick testing. For real applications, use environment variables.
GEMINI_API_KEY = "AIzaSyAE3qIXXkEoLdugrDzgtStC6iWQChvBWL4" # <--- PASTE YOUR ACTUAL GEMINI API KEY HERE!


recognizer = sr.Recognizer()

engine = pyttsx3.init()

# Initialize your Jarvis AI Agent (Gemini powered)
# Pass the hardcoded API key to the agent
jarvis_ai = PersonalAIAgent(GEMINI_API_KEY)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    command_lower = c.lower()
    print(f"Processing command: {command_lower}") # Added for debugging

    if "open google" in command_lower:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "open instagram" in command_lower:
        speak("Opening Instagram.")
        webbrowser.open("https://instagram.com")
    elif "open youtube" in command_lower:
        speak("Opening YouTube.")
        # Corrected YouTube URL - your original had a googleusercontent.com prefix
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command_lower:
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")
    elif "open spotify" in command_lower:
        speak("Opening Spotify.")
        # Corrected Spotify URL - your original had a googleusercontent.com prefix
        webbrowser.open("https://spotify.com")
    elif command_lower.startswith("play"):
        song_name = command_lower.replace("play", "").strip()
        if song_name in music_library.music:
            speak(f"Playing {song_name}.")
            webbrowser.open(music_library.music[song_name])
        else:
            speak(f"Sorry, I couldn't find {song_name} in your music library.")
    else:
        # If no specific command matches, send the query to Gemini
        speak("Let me think...")
        gemini_response = jarvis_ai.get_response(c)
        speak(gemini_response)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for wake word "Jarvis"
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                # Adjust for ambient noise once at the start of listening
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=3, phrase_time_limit=2) # Increased limits for robustness

            # Use 'in' for robustness against slight variations in pronunciation
            word = r.recognize_google(audio).lower()
            print(f"Heard wake word: '{word}'") # For debugging

            if "jarvis" in word:
                speak("Yes sir?")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active. Listening for command...")
                    r.adjust_for_ambient_noise(source, duration=0.5) # Adjust again for command
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except sr.UnknownValueError:
            # print("Could not understand audio, waiting for Jarvis...") # Uncomment for debugging
            pass # Silently continue listening if "Jarvis" isn't heard clearly
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition service; {e}")
            print(f"Speech recognition error: {e}") # Log error for debugging
        except Exception as e:
            speak(f"An unexpected error occurred: {e}")
            print(f"General error in main loop: {e}") # Log error for debugging