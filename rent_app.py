#RENT CLASSIFICATOR
import joblib
import streamlit as st
import pandas as pd
import numpy as np

# Loading the trained model
with open('model.joblib', 'rb') as pickle_in:
    gbc = joblib.load(pickle_in)

#page configurationn
st.set_page_config(page_title="Rent verifier madrid", layout="wide", page_icon="🏢")

# defining the function which will make the prediction using the data which the user inputs TRANSFORMATIONS & RUNNING MODEL
def prediction(Rooms, Squared_meters, Floor, Distric, Type, Pool, Furniture, Exterior, Elevator):

    # Pre-processing user input    
    if Pool == "No":
        Pool = 0
    else:
        Pool = 1

    if Furniture == "No":
        Furniture = 0
    else:
        Furniture = 1

    if Elevator == "No":
        Elevator = 0
    else:
        Elevator = 1

    if Exterior == "No":
        Exterior = 0
    else:
        Exterior = 1

    ################################

    data = {
        "Rooms": Rooms,
        "Squared_meters": Squared_meters,
        "Floor": Floor,
        "Distric": Distric,
        "Type": Type,
        "Pool": Pool,
        "Furniture": Furniture,
        "Exterior": Exterior,
        "Elevator": Elevator
    }

    # Convert data into dataframe
    df = pd.DataFrame.from_dict([data])
    predicted_value = float(gbc.predict(df)[0])

    return predicted_value


##############################

# This is the main function in which we define our webpage FRONT END 
def main():       
    # Front-end elements of the web page 
    html_temp = """
    <div style="background-color:papayawhip;padding:10px">
    <h2 style="color:black;text-align:center;">Rent Verifier Madrid</h2>
    </div>"""

    st.markdown(html_temp, unsafe_allow_html=True)

    st.image("image5.jpg")

    # Create a subheader
    st.subheader("Confirm if your property's monthly rent value is above 850 EUR")

    # Create a markdown with details about the app
    st.markdown(
        """
        ## About the app

        This app predicts if a property in Madrid can be rented for >850 EUR or not.

        ## About the data

        The data was collected through Idealista in 2022.

        ## About the model

        The model was trained using an Gradient Booster Classifier.
        """
    )

    # Create a text prompt
    st.title("Please fill the form below")

 
################################
          
    # Following lines create input fields for prediction 
    Rooms = st.slider('Rooms in the property', 1, 4, 1)
    Squared_meters = st.number_input("Property Squared Meters") 
    Floor = st.slider('What floor is the property located?', 0, 6, 1)
    
    districts = ('Malasaña', 'Moncloa', 'Lavapies', 'Chueca', 'Chamartin', 'La Latina')
    Distric = st.selectbox('What district is your property located?', districts)

    types = ('Flat', 'Studio', 'Duplex', 'Attic')
    Type = st.selectbox('Which is the type of your property?', types)

    Pool = st.selectbox('Does the property have a pool?', ("Yes", "No"))
    Furniture = st.selectbox('Is the property furnished?', ("Yes", "No"))
    Exterior = st.selectbox('Is the property exterior?', ("Yes", "No"))
    Elevator = st.selectbox('Does the property have an elevator?', ("Yes", "No"))

    result = ""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Rooms, Squared_meters, Floor, Distric, Type, Pool, Furniture, Exterior, Elevator)
        
        if result == 0:
            pred = 'No, your property monthly rent is not valued above 850 EUR.'
            st.warning(pred)
        else:
            pred = 'Yes, your property monthly rent is valued above 850 EUR.'
            st.success(pred)
        
      
if __name__ == '__main__': 
    main()