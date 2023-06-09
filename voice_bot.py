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

