import pandas as pd
import os

def clean_file(file_path):
    ''' preprocessing of the raw data 
    making it digestible by the model
    
    input : path to the raw csv
    output : the path were the cleaned csv is stored'''

    #import data in a dataframe
    data = pd.read_csv(file_path)

    #there must be a nicer way to do this
    data = data.rename(columns={
        "Customer Type": "Customer_Type",
        "Type of Travel": "Type_of_Travel",
        "Flight Distance": "Flight_Distance",
        "Inflight wifi service": "Inflight_wifi_service",
        "Departure/Arrival time convenient": "Departure_Arrival_time_convenient",
        "Ease of Online booking": "Ease_of_Online_booking",
        "Food and drink": "Food_and_drink",
        "Online boarding": "Online_boarding",
        "Seat comfort": "Seat_comfort",
        "Inflight entertainment": "Inflight_entertainment",
        "On-board service": "On_board_service",
        "Leg room service": "Leg_room_service",
        "Baggage handling": "Baggage_handling",
        "Checkin service": "Checkin_service",
        "Inflight service": "Inflight_service",
        "Departure Delay in Minutes": "Departure_Delay_in_Minutes",
        "Arrival Delay in Minutes": "Arrival_Delay_in_Minutes"
    })

    #drop the missing delay
    data = data.dropna()
    #combining departure and arrival delay
    data['Total_Delay'] = data['Departure_Delay_in_Minutes'] + data['Arrival_Delay_in_Minutes']
    #we won't need that anymore
    data=data.drop(['Departure_Delay_in_Minutes'], axis=1)
    data=data.drop(['Arrival_Delay_in_Minutes'], axis=1)
    data=data.drop(['id'], axis=1)
    #mapping the result of the survey
    data['Satisfaction'] = data['Satisfaction'].map({'neutral or dissatisfied': 0, 'satisfied': 1})
    #One hot encoding of categorical values
    data = pd.get_dummies(data, columns=['Gender', 'Customer_Type', 'Type_of_Travel', 'Class'])

    #saving
    exit_path = os.path.join(os.path.dirname(file_path), 'data_cleaned.csv')
    data.to_csv(exit_path, index=False)

    return exit_path