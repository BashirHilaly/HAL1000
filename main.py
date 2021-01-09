import os
import pyttsx3
import datetime
import time
import wikipedia
import speech_recognition as sr
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Talk to replika
replikaSite = "https://my.replika.ai/login"
driver = webdriver.Chrome(ChromeDriverManager().install())
# Login Info
emailOrPhone = "EMAIL FOR REPLIKA ACCOUNT"
password = "PASSWORD FOR REPLIKA ACCOUNT"



male = 0
female = 1

engine = pyttsx3.init('sapi5')

voice = engine.getProperty('voices') # getting properties of the voice

engine.setProperty('voice', voice[male].id)


# Function for speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait() # For audible speech

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")



# Takes microphone input from the user and returns string output
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = .5
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")  #User query will be printed.
    except Exception as e:
        # print(e)  use only if you want to print the error!
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

def converse(query):
    inputText = driver.find_element_by_id("send-message-textarea")
    inputText.clear()
    inputText.send_keys(query)
    inputText.send_keys(Keys.ENTER)



if __name__=="__main__" :
    driver.get(replikaSite)
    #Login
    userElem = driver.find_element_by_id("emailOrPhone")
    userElem.send_keys(emailOrPhone)
    userElem.send_keys(Keys.ENTER)
    time.sleep(4)
    passwordElem = driver.find_element_by_id("login-password")
    passwordElem.clear()
    passwordElem.send_keys(password)
    passwordElem.send_keys(Keys.ENTER)
    time.sleep(5)
    acceptCookies = driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[1]/button")
    acceptCookies.click()
    wishMe()

    # Send Input and retrieve output

    while True:
        query = takeCommand().lower() #Converting user query into lower case
        
        # Logic for executing tasks based on query
        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) 
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open Application(s)
        elif 'FILE NAME' in query:
            os.startfile(r"FILE PATH")
            speak(results)
        # Tell the time
        elif 'what time is it' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"The time is {strTime}")

        # Send Input and adjust conversation position
        elif query != "none":
            converse(query)
            time.sleep(8)
            # check if response exists
            responses = driver.find_elements_by_xpath("//span[@aria-label='HAL 1000 says:']")
            print(responses[-1].text)
            speak(responses[-1].text)
        else:
            pass