import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Components.Process_data import clean_file
import os

#Sidebar switch
tabs = st.sidebar.radio("Select an UI :", ("DashBoard Data", "Prediction"))

if tabs =='DashBoard Data':
    st.subheader('Dashboard Data')

    #Generatif clean csv
    # TODO : Logic check if csv not exists
    dir_path = os.path.abspath(os.path.dirname(__file__))
    input_filepath = os.path.join(dir_path, 'Data/Airline_Dataset.csv')
    clean_file_path = clean_file(input_filepath)

    file = st.select_slider('Select Data File', ['Cleaned', 'Raw'])
    #Loading Cleaned CSV
    if file == 'Cleaned':
        data = pd.read_csv(clean_file_path)
    elif file == 'Raw':
        data = pd.read_csv(input_filepath)

    # #Plotting scatterplot
    # st.subheader('Scatter it')

    # #Columns choice 
    # selected_x = st.selectbox('Select abcissa : ', data.columns)
    # selected_y = st.selectbox('Select ordinate : ', data.columns)

    # if selected_x and selected_y:
    #     fig, ax = plt.subplots()
    #     sns.scatterplot(data=data, x=selected_x, y=selected_y, ax = ax)
    #     st.pyplot(fig)

    # #plotting hist
    # # TODO : checkbox to use log scale
    # st.subheader('Distribute it')
    # selected_num_column = st.selectbox("Select a numerical:", data.select_dtypes('number').columns)
    # bins = st.slider('Bins number', min_value=1, max_value=500)
    # log = st.checkbox('Use Logarithmic scaling')

    # fig,ax = plt.subplots()
    # plt.hist(data[selected_num_column], bins = bins,log=log)
    # st.pyplot(fig)


    #choose plot?
    st.subheader('Catplot')
    plot_type = st.selectbox('Type of plot', options=['strip','violin', 'box', 'count'])
    selected_x = st.selectbox('Select abcissa : ', data.columns, key='x_2')
    selected_y = st.selectbox('Select ordinate : ', data.columns, key='y_2')
    selected_z = st.selectbox('Select a category is you need : ', data.columns)

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
        gender = row[0].selectbox('Gender', ['Male', 'Female'])
        customer_type = row[0].selectbox('Customer Type', ['Loyal', 'Disloyal'])
        travel_type = row[1].selectbox('Type of travel', ['Business', 'Personnal'])
        age = row[0].slider('Age', min_value=5, max_value=80, value=30)
        travel_class = row[1].selectbox('Class', ['Business', 'Eco', 'Proletarian'])
        distance = row[1].slider('Flight distance (miles?)', min_value=30, max_value=5000, value=500)
        delay = st.slider('Delay (minutes)', min_value=0, max_value=2000)

        submit = st.form_submit_button('Request Prediction')





    


