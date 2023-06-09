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
