import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Components.Process_data import clean_file
import os
from Components.Predict_cat import predict_satisfaction
from catboost import CatBoostClassifier

#Sidebar switch
tabs = st.sidebar.radio("Select an UI :", ("DashBoard Data", "Prediction"))

if tabs =='DashBoard Data':
    st.subheader('Dashboard Data')
    #load clean or raw csv
    # TODO : Logic check if csv not exists
    dir_path = os.path.abspath(os.path.dirname(__file__))
    input_filepath = os.path.join(dir_path, 'Data/satisfaction_customers_export.csv')
    clean_file_path = clean_file(input_filepath)

    file = st.select_slider('Select Data File', ['Raw', 'Cleaned'])
    #Loading Cleaned CSV
    if file == 'Cleaned':
        data = pd.read_csv(clean_file_path)
    elif file == 'Raw':
        data = pd.read_csv(input_filepath)

    graph1, graph2, graph3 = st.tabs(['Simple Scatter plot', 'Histogram', 'Custom plot'])
    
    with graph1:
        #Plotting scatterplot
        st.subheader('Scatter it')

        #Columns choice 
        selected_x = st.selectbox('Select abcissa : ', data.columns)
        selected_y = st.selectbox('Select ordinate : ', data.columns)

        if selected_x and selected_y:
            fig, ax = plt.subplots()
            sns.scatterplot(data=data, x=selected_x, y=selected_y, ax = ax)
            st.pyplot(fig)  

    with graph2:
        #plotting hist
        st.subheader('Distribute it')
        selected_num_column = st.selectbox("Select a numerical:", data.select_dtypes('number').columns)
        bins = st.slider('Bins number', min_value=1, max_value=500)
        log = st.checkbox('Use Logarithmic scaling')

        fig,ax = plt.subplots()
        plt.hist(data[selected_num_column], bins = bins,log=log)
        st.pyplot(fig)

    with graph3:
        #choose plot?
        st.subheader('Catplot')
        plot_type = st.selectbox('Type of plot', options=['strip','violin', 'box', 'count'])
        selected_x = st.selectbox('Select abcissa : ', data.columns, key='x_2')
        selected_y = st.selectbox('Select ordinate : ', data.columns, key='y_2')
        if st.toggle('Third category as hue'):
            selected_z = st.selectbox('Select a category if you need it : ', data.columns)
        else:
            selected_z = None
            hue = None

        if plot_type and selected_x and selected_y:
            if selected_z:
                hue = selected_z
            if plot_type  =='count':
                fig, ax = plt.subplots()
                fig = sns.catplot(data=data, x=selected_x, hue=hue, kind=plot_type)
                st.pyplot(fig)
            else:
                orientation = st.select_slider('Graph Orientation', ['vertical', 'horizontal'])
                fig, ax = plt.subplots()
                fig = sns.catplot(data=data, x=selected_x, y=selected_y, hue=hue, kind=plot_type, orient=orientation)
                st.pyplot(fig)


if tabs =='Prediction':
    #Prediction Form
    st.header('Input Parameters')
    st.subheader('Describe your usual suspect')

    with st.form('Inputs'):
        header = st.columns(2)
        header[0].subheader('Client')
        header[1].subheader('Flight')

        row = st.columns(2)
        gender_select = row[0].selectbox('Gender', ['Male', 'Female']) 
        customer_type_select = row[0].selectbox('Customer Type', ['Loyal', 'Disloyal']) 
        travel_type_select = row[1].selectbox('Type of travel', ['Business', 'Personnal']) 
        age = row[0].slider('Age', min_value=5, max_value=80, value=30)
        travel_class_select = row[1].selectbox('Class', ['Business', 'Eco', 'Proletarian']) 
        distance = row[1].number_input('Flight distance (miles?)', min_value=30, max_value=5000, value=500)
        delay = st.number_input('Delay (minutes)', min_value=0, max_value=2000)
        # expand_form = st.toggle('Simulate a satisfaction form')
        # if expand_form:
        st.subheader('Form')
        row2 = st.columns(3)
        time_convenience = row2[0].slider('Departure/Arrival time convenient', min_value=0,max_value=5)
        booking_ease = row2[1].slider('Ease of Online booking', min_value=0,max_value=5)
        gate = row2[2].slider('Gate location', min_value=0,max_value=5)
        coca = row2[0].slider('Food and drink', min_value=0,max_value=5)
        online_boarding = row2[1].slider('Online boarding', min_value=0,max_value=5)
        comfort = row2[2].slider('Seat comfort', min_value=0,max_value=5)
        entertainment = row2[0].slider('Inflight entertainment', min_value=0,max_value=5)
        onboard_service = row2[1].slider('On-board service', min_value=0,max_value=5)
        leg = row2[2].slider('Leg room service', min_value=0,max_value=5)
        bagage = row2[0].slider('Baggage handling', min_value=1,max_value=5) #why
        checkin = row2[1].slider('Checkin service', min_value=0,max_value=5)
        inflight_service = row2[2].slider('Inflight service', min_value=0,max_value=5)
        clean = row2[0].slider('Cleanliness', min_value=0,max_value=5)
        wifi = row2[1].slider('Inflight Wifi Service', min_value=0,max_value=5)
        submit = st.form_submit_button('Request Prediction')

    #mapping categorical values in a unelegant way
    if gender_select == 'Male':
        male=1
        female=0
    else:
        male=0
        female=1

    if customer_type_select =='Loyal':
        cust_type_loyal = 1
        cust_type_dis = 0
    else: 
        cust_type_loyal = 0
        cust_type_dis = 1

    if travel_type_select =='Business':
        travel_type_business = 1
        travel_type_perso = 0
    else: 
        travel_type_business = 0
        travel_type_perso = 1
    
    if travel_class_select =='Business':
        travel_class_business = 1
        travel_class_eco = 0
        travel_class_ecoplus = 0
    elif travel_class_select == 'Eco':
        travel_class_business = 0
        travel_class_eco = 1
        travel_class_ecoplus = 0
    else:
        travel_class_business = 0
        travel_class_eco = 0
        travel_class_ecoplus = 1

    #dict of varaibles
    passanger_data = pd.DataFrame( { 'Age' : [age], 
                                    'Flight_Distance' : [distance],
                                    'Inflight_wifi_service' : [wifi] ,
                                    'Departure_Arrival_time_convenient' : [time_convenience], 
                                    'Ease_of_Online_booking' : [booking_ease],
                                    'Gate_location' : [gate],
                                    'Food_and_drink' : [coca], 
                                    'Online_boarding' : [online_boarding],
                                    'Seat_comfort' : [comfort],
                                    'Inflight_entertainment' : [entertainment], 
                                    'Ease_of_Online_booking' : [booking_ease],
                                    'On_board_service' : [onboard_service], 
                                    'Leg_room_service' : [leg],
                                    'Baggage_handling' : [bagage], 
                                    'Checkin_service' : [checkin], 
                                    'Inflight_service' : [inflight_service],
                                    'Cleanliness' : [clean], 
                                    'Total_Delay' : [delay],
                                    'Gender_Female': [female],
                                    'Gender_Male': [male],
                                    'Customer_Type_Loyal Customer': [cust_type_loyal] ,
                                    'Customer_Type_disloyal Customer' : [cust_type_dis],
                                    'Type_of_Travel_Business travel' : [travel_type_business],	
                                    'Type_of_Travel_Personal Travel' : [travel_type_perso],
                                    'Class_Business' : [travel_class_business]	,
                                    'Class_Eco' : [travel_class_eco]	,
                                    'Class_Eco Plus' : [travel_class_ecoplus] ,
                                    })
    
    if submit:
        # st.write(passanger_data)
        model = CatBoostClassifier()
        #loading the model
        dir_path = os.path.abspath(os.path.dirname(__file__))
        modelpath = os.path.join(dir_path, 'ML/meilleur_modele_catboost.model')
        model.load_model(modelpath)
        #predict the outcome
        pred, proba = predict_satisfaction(model, passanger_data)
        
        if pred == 1:
            st.success('Yey A pleased customer!')
        elif pred == 0:
            st.warning('Git Gud')
        else:
            st.error('Something went wront')
        proba_df = pd.DataFrame(proba, columns=['Unsatisfied probability', 'Satisfied Probability'])
        # st.dataframe(proba_df)
        fig2, ax2 = plt.subplots()
        fig2 = sns.catplot(data=proba_df, kind='bar', orient='y', aspect=2)
        st.pyplot(fig2)

        with st.expander('Feature Importance', expanded=False):
            feature_importance = model.get_feature_importance()
            fig3, ax3 = plt.subplots()
            plt.barh(passanger_data.columns, feature_importance)
            st.pyplot(fig3)





        