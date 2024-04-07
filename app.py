from flask import Flask, request, jsonify, render_template, session
import speech_recognition as sr
import webbrowser
import datetime
from sk import *
import re
import wikipedia
from features import *
import pyttsx3
from gmail import *


app = Flask(__name__,static_url_path='/static')
app.secret_key = 'pakhi'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get-information', methods=['POST'])
def get_information():
    if request.method == 'POST':
        data = request.get_json()
        query = data['query'].lower()
        response_text = ""

        try:
            ## list of website that you want to access
            done=False
            sites=[["Wikipedia","https://www.wikipedia.org/"],["leetcode","https://www.leetcode.com"],["linkedin","https://www.linkedin.com"],["instagram","https://www.instagram.com"],
                   ["github" , "https://www.github.com"],["facebook", "https://www.facebook.com"],['hackerrank',"https://www.hackerrank.com"],['snapchat',"https://www.snapchat.com/"],
                   ["stackoverflow" , "https://stackoverflow.com/"],["spotify" , "https://open.spotify.com/"],["amazon","https://www.amazon.com/"]]

            for site in sites: 
               if f"open {site[0]}".lower() in query:
                  speak(f"Opening {site[0]}..")
                  webbrowser.open(site[1])
                  done=True
            
            if 'hello' in query or 'Namaste' in query:
                speak("Hello, Good Day, welcome to Zira, How can i help you?")
                response_text = "How can i help you"
                done=True

            # Welcome
            elif 'thanks' in query:
                speak('Pleasure to help you')
                done=True

            elif 'thank you' in query:
                speak('Pleasure to help you') 
                done=True
            
            elif "who i am" in query:
                speak("If you talk then definitely your human.")
                done=True
            elif "why you came to world" in query:
                speak("Thanks to Gaurav. further It's a secret")
                done=True
            elif 'reason for you' in query:
                speak("I was created for human ease ") 
                done=True   
            #time
            elif 'time' in query:
                hour = int(datetime.datetime.now().strftime("%H"))
                min = int(datetime.datetime.now().strftime("%M"))
                if hour < 12:
                   am_pm = 'AM'
                else:
                   am_pm = 'PM'
        
                hour = hour % 12
                if hour == 0:
                   hour = 12
                speak(f"It's {hour} : {min}  {am_pm}")
                done=True
            
            #Date
            elif 'date' in query or 'day' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {current_date}")
                done=True  

            #Name
            elif 'what is your name' in query:
                  speak(name)
            elif 'what\'s your name' in query:
                  speak(name)
            elif 'your name' in query:
                  speak(name)

            # Open google
            elif 'open google' in query:
                 if 'search' in query:
                    search_query = query.split('open google and search')[-1].strip()
                    search_google(search_query)
                    speak(f"Searching Google for {search_query}")
                 else:
                    webbrowser.open("https://www.google.com/")
                    speak('Opening Google...')
                 done=True

            elif 'open google maps' in query: 
                if 'search' in query:
                    search_query = query.split('open google maps and search')[-1].strip()
                    search_google_maps(search_query)
                    speak(f"Searching on google maps for {search_query}")
                else:
                    webbrowser.open("https://www.google.com/maps/")
                    speak('Opening google maps...')
                done=True
            
            #Open Youtube
            elif 'open youtube' in query:
                if 'search' in query:
                    search_query = query.split('open youtube and search')[-1].strip()
                    search_youtube(search_query)
                    speak(f"Searching on youtube for {search_query}")
                else:
                    webbrowser.open("https://www.youtube.com/")
                    speak('Opening youtube...')
                done=True
            
            #wikipedia
            elif 'search' in query:  
                speak('Searching Wikipedia...')
                query = query.replace("search", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to Wikipedia")
                print(results)
                speak(results)
                done=True  

            #play song
            elif 'play music' in query or 'play song' in query or 'play' in query:
                play_music()
                speak('Playing music...')
                done=True
            
            
            elif 'speed' in query:
                speed = int(query.split()[-1])
                speak("Voice speed changed", speed=speed)
                done=True


            #for weather
            elif 'weather' in query:
             try:
                city = re.search(r"(in|of|for) ([a-zA-Z]*)", query)
                if city:
                    city = city[2]
                    weather = get_weather_info(city)
                    speak(weather)
                else:
                    weather = get_weather_info()
                    speak(weather)  
             except:
                 speak("City does not found")  
                 done=True

            #for ip address
            elif "ip address" in query:
                 ip = get_ip()
                 if ip:
                    speak(ip)
                    done = True 

            #for news
            elif 'news' in query or 'current affairs' in query:
              speak(" Sure...., here are some top news")
              arr=news()
              for i in arr:
                  speak(i)
              done=True   

            #for news                   
            elif 'joke' in query or 'jokes' in query:
                speak("Sure, get ready for some chuckles")
                arr=joke()
                speak(arr[0])
                speak(arr[1])
                done=True
            
            #for remember
            elif 'reminder' in query or 'remind me' in query:
                set_reminder()
                done=True

            # Read Remember
            elif 'read remember' in query or 'remember' in query:
                 speak('Yes..')
                 read_remember()
                 done=True 
            elif 'what do you remember' in query:
                speak('Yes..')
                read_remember()
                done=True 
            elif 'do you remember' in query:
                speak('Yes..')
                read_remember()
                done=True 
            
            elif 'who are you' in query:
                speak("I am virtual assistant created by Pakhi")
                done=True
                  
            # search for google
            elif 'open google and search' in query:
                search_query = query.split('open google and search')[-1].strip()
                search_google(search_query)
                speak(f"Searching Google for {search_query}")
                done=True
            
            elif 'open youtube and search' in query:
                search_query = query.split('open youtube and search')[-1].strip()
                search_youtube(search_query)
                speak(f"Searching YouTube for {search_query}")
                done=True
            
            ## for map
            elif "distance" in query or "map" in query:
                #search_query = query.split('open google maps and search')[-1].strip()
                speak(f"Searching Google Maps for {query}")
                search_google_maps(query)
                done=True

            #for movies  
            elif "movies" in query or "movie" in query:
                 speak("Some of the latest popular movies are as follows :")
                 get_popular_movies()
                 done=True

            elif "bye bye" in query or "stop" in query:
                 speak("Goodbye, have a nice day")
                 done=True

            elif "write" in query:
                 ##speak("The task is saved in directory....")
                 speak("Here are some result:..")
                 response_text=ai(query)
                 done=True   

            elif "send email" in query:

               speak("Speak the receiver id : ")
               e= get_user_response()
               receiver_id =preprocess_spoken_email(e)
               
               while not check_email(receiver_id):
                     speak("Invalid email id\nType reciever id again : ")
                     receiver_id = get_user_response()     
               speak("Tell the subject of email")
               subject = get_user_response()
               speak("tell the body of email")
               body = get_user_response()
               success = send_email(receiver_id, subject, body)
               if success:
                  speak('Email sent successfully')
               else:
                  speak("Error occurred while sending email")
               done = True              

            
            elif "send gmail to everyone" in query:
                  speak("Sure, Tell the email subject:")
                  subject = get_user_response()
                  speak("Tell the email body...")
                  body = get_user_response()
                  speak("Sending email to everyone...")
                  send_everyone(subject, body)
                  speak("Emails sent successfully!")
                  done = True
            
            elif "sing a song" in query:
                speak('I am sorry for any confusion, but I am just play the song and do not have the ability to sing')

            elif 'none' in query:
                speak("Sorry, I didn't catch that command.")
                done=True

            elif "jeera" in query:
                speak("HelLo... this is my name")
                done=True
            
            else:
                if not done: 
                 response=chatBot(query)
                 response_text = response
                 lines = response.split('\n')
                for line in lines[:2]:
                         speak(line)  

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
            response_text = "Sorry"
        except sr.RequestError:
            speak("Sorry, there was an error processing your request.")
            response_text = "Sorry"
            
        return jsonify({'status': 'success','response_text': response_text})
    

if __name__ == '__main__':
   
    app.run(debug=True)