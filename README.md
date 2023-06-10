# <p align="center">TICKET BOOKING BOT FOR THE VISUALLY IMPAIRED

## *Introduction* :
Booking ticket for the Visually Impaired requires human assistance which makes them dependent on others all the time. In the modern era, technological advancements is growing at a rapid speed. So, with the use of an ticket booking bot we can make process of booking tickets easier for the Visually Impaired.
  
## _Purpose of the Project_ :
The sole purpose of this project is to make the Visually Impaired both independent of others and the process of booking tickets easier. Our bot makes it easier for them and they can book tickets by themselves on their mobile phone in just minutes using voice recognition. By doing so they can book tickets by themselves and reduces their dependency on others.
  
## _Objective_ :
Ticket Booking Bot for the Visually Impaired project is to develop a user-friendly and accessible automated system that allows visually impaired individuals to book tickets for various modes of transportation, such as flights, trains, buses, or movies, with ease and independence. The project aims to leverage artificial intelligence and natural language processing techniques to create a conversational interface that understands and responds to the specific needs of visually impaired users. By providing a seamless and inclusive ticket booking experience, the project aims to enhance the accessibility and independence of visually impaired individuals, empowering them to travel and participate in various activities with greater convenience and confidence. 
  
## _Abstract_ :
The Ticket Booking Bot for the Visually Impaired project aims to create an accessible and inclusive ticket booking system for individuals with visual impairments. By utilizing artificial intelligence and natural language processing, the project seeks to develop a conversational interface that understands and responds to the specific needs of visually impaired users. The bot will enable users to search for and book tickets for various modes of transportation and entertainment activities through voice commands or text input. Integration with ticketing platforms and databases will ensure real-time availability and accurate information retrieval. Ultimately, the project aims to enhance the independence and convenience of visually impaired individuals in booking tickets, promoting inclusivity and equal access to travel and entertainment experiences.

## _Methodology_ :
  + Collect the data about the individual initially.
  
  - Now store the collected data in the database.
  
  * Their individual data will be stored in the database.

  - They can now give the details about the destination, their travel data & time and all necessary details.

  - The bot will go to the ticket booking website and look for the specifications and fills the details and books the ticket.

  - It will now give the ticket details back to the user.
  
## _Project Architecture_ :
<img width="278" alt="mini project" src="https://github.com/vigneshwar-24/TICKET-BOOKING-BOT-FOR-THE-VISUALLY-IMPAIRED/assets/77089276/1005ce54-1db9-45b1-8c7f-db9af003a5c9">

  
## _Program_ :
### voice_bot.py
```python
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

def recognize_speech():
    try:
        with sr.Microphone() as mic:
            r.adjust_for_ambient_noise(mic, duration=0.8)
            audio = r.listen(mic)
            text = r.recognize_google(audio)
            return text.lower()
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("No speech detected")
        return None

def get_user_details():
    name = None
    age = None
    aadhar_number = None

    while not all([name, age, aadhar_number]):
        if name is None:
            SpeakText("What is your name?")
            name = recognize_speech()
            if name:
                SpeakText("Your name is " + name)

        if age is None:
            SpeakText("What is your age?")
            age = recognize_speech()
            if age:
                SpeakText("Your age is " + age)

        if aadhar_number is None:
            SpeakText("What is your Aadhar number?")
            aadhar_number = recognize_speech()
            if aadhar_number:
                SpeakText("Your Aadhar number is " + aadhar_number)

    return {
        'name': name,
        'age': age,
        'aadhar_number': aadhar_number,
    }



def get_travel_details():
    from_place = None
    to_place = None

    while not all([from_place, to_place]):
        SpeakText("Please provide your travel details.")
        if from_place is None:
            SpeakText("What is the source location?")
            from_place = recognize_speech()
            if from_place:
                SpeakText("Source location is " + from_place)

        if to_place is None:
            SpeakText("What is the destination location?")
            to_place = recognize_speech()
            if to_place:
                SpeakText("Destination location is " + to_place)
    
    return {
        'from_place': from_place,
        'to_place': to_place,
    }

```
 
  
### booking.py
```python
import json
from voice_bot import get_travel_details, get_user_details, SpeakText, recognize_speech
from PIL import Image, ImageDraw, ImageFont


# Function to search for matching trains based on source and destination
def search_trains(source, destination):
    matched_trains = []
    for train in train_data:
        if train['Source'].lower() == source.lower() and train['Destination'].lower() == destination.lower():
            matched_trains.append(train)
    else:
        SpeakText("There are no trains available. Sorry I hope you could use another mode of transport")
        return None
    return matched_trains


def generate_ticket(ticket_data):
    # Create a blank ticket image
    ticket_image = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(ticket_image)

    # Set up fonts
    title_font = ImageFont.truetype('arial.ttf', size=24)
    content_font = ImageFont.truetype('arial.ttf', size=16)

    # Draw ticket content
    draw.text((50, 50), f"Name: {user_details['name']}", font=content_font, fill='black')
    draw.text((50, 80), f"Age: {user_details['age']}", font=content_font, fill='black')
    draw.text((50, 110), f"Aadhar Number: {user_details['aadhar_number']}", font=content_font, fill='black')
    draw.text((50, 140), f"Train Name: {ticket_data['Train_Name']}", font=content_font, fill='black')
    draw.text((50, 170), f"Train Number: {ticket_data['Train_num']}", font=content_font, fill='black')
    draw.text((50, 200), f"Seat Number: D45", font=content_font, fill='black')
    draw.text((50, 230), f"Timings: {ticket_data['Timings']}", font=content_font, fill='black')

    # Save the ticket image
    ticket_image.save('ticket.png')
    SpeakText(f"Train Name is {ticket_data['Train_Name']}, train number is {ticket_data['Train_num']} and train timings is {ticket_data['Timings']} ")
    SpeakText("Ticket is generated. I hope you enjoy your ride and make sure to arrive at the station before half an hour.")

def book(train):
    SpeakText("Do you want me to book the train?")
    print("Do you want me to book the train?")
    if recognize_speech().lower() == 'yes':
        print("Train booked successfully.")
        SpeakText("Train booked successfully.")
        generate_ticket(train)  # Pass the train details instead of user_details
    else:
        print("Okay. I hope I was of good assistance to you. Thank you.")
        SpeakText("As you wish. I hope I was of good assistance to you. If you wanna book tickets do ask to me. Thank you.")
        
def classify_timings(timings):
    hour = int(timings.split(':')[0])

    if 0 <= hour <= 11:
        return 'morning'
    elif 12 <= hour <= 16:
        return 'afternoon'
    elif 17 <= hour <= 18:
        return 'evening'
    elif 19 <= hour <= 23:
        return 'night'
    else:
        return 'Invalid Timings'


def logic_checking():
    if matched_trains == None:
        return 1
    if len(matched_trains) == 0:
        SpeakText("Sorry, no train is found. Can't book the train.")
    else:
        if len(matched_trains) == 1:
            SpeakText(f"There is only one train available and the timing is {matched_trains[0]['Timings']}")
            book(matched_trains[0])
            return 1 
        else:
            slot = []
            SpeakText(f"There are {len(matched_trains)} trains available. Which one do you want to book?")
            for i, train in enumerate(matched_trains):
                timings = train['Timings']
                SpeakText(f"{i + 1}. {train['Train_Name']}")
                classification = classify_timings(timings)
                slot.append(classification)
                SpeakText(f"{classification} train")

            while True:
                user_choice = SpeakText("Tell me which train slot you want? (morning, afternoon, evening, night)")
                inde = recognize_speech().lower()
                if all(item.lower() != inde for item in slot):
                    print('The selected slot has no train available. Please try again')
                    SpeakText("The selected slot has no train available. Please try again.")
                else:
                    book(matched_trains[slot.index(inde)])
                    return 1


if __name__ == '__main__':

    user_details = get_user_details()
    travel_details = get_travel_details()
    
    print("User Details:", user_details)
    print("Travel Details:", travel_details)

    # Load the train data from the file
    with open('IRCTC/train.json') as file:
        train_data = json.load(file)
        
    source =  travel_details['from_place']
    destination = travel_details['to_place']
    
    

    # Search for matching trains
    matched_trains = search_trains(source, destination)

    if logic_checking() == 1:
        pass
    else:
        logic_checking()
``` 

## Output:
![ticket](https://github.com/vigneshwar-24/TICKET-BOOKING-BOT-FOR-THE-VISUALLY-IMPAIRED/assets/75234646/68f83354-d0fa-4811-9897-81860ac17d68)

## _Conclusion_ :
With the aid of this bot, the process will be easier and much more faster over the existing way of ticket booking. It improves their way of living and technological advancement is applied in a way that everyone can improve their standard of living.

## _Results_ :
  **->** Faster and efficient way of ticket booking for the Visually Impaired.

  **->** Reduces time consumption and mediation of other humans.

  **->** Can book the ticket in minutes.

  **->** No sharing of personal data to others.
  
  **->** Booking tickets by themselves along with the bot.
