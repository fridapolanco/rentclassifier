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
def prediction(rooms,squared_meters, floor, distric, type, pool, furniture, exterior, elevator):

    # Pre-processing user input    
    if pool == "No":
        pool = 0
    else:
        pool = 1

    if furniture == "No":
        furniture = 0
    else:
        furniture = 1

    if elevator == "No":
        elevator = 0
    else:
        elevator = 1

    if exterior == "No":
        exterior = 0
    else:
        exterior = 1

    ################################

    data = {
        "Rooms": rooms,
        "Squared_meters": squared_meters,
        "Floor": floor,
        "Distric": distric,
        "Type": type,
        "Pool": pool,
        "Furniture": furniture,
        "Exterior": exterior,
        "Elevator": elevator
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
    rooms = st.slider('Rooms in the property', 1, 4, 1)
    squared_meters = st.number_input("Property Squared Meters") 
    floor = st.slider('What floor is the property located?', 0, 6, 1)
    
    districts = ('Malasaña', 'Moncloa', 'Lavapies', 'Chueca', 'Chamartin', 'La Latina')
    distric = st.selectbox('What district is your property located?', districts)

    types = ('Flat', 'Studio', 'Duplex', 'Attic')
    type = st.selectbox('Which is the type of your property?', types)

    pool = st.selectbox('Does the property have a pool?', ("Yes", "No"))
    furniture = st.selectbox('Is the property furnished?', ("Yes", "No"))
    exterior = st.selectbox('Is the property exterior?', ("Yes", "No"))
    elevator = st.selectbox('Does the property have an elevator?', ("Yes", "No"))

    result = ""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(rooms, squared_meters, floor, distric, type, pool, furniture, exterior, elevator)
        
        if result == 0:
            pred = 'No, your property monthly rent is not valued above 850 EUR.'
            st.warning(pred)
        else:
            pred = 'Yes, your property monthly rent is valued above 850 EUR.'
            st.success(pred)
        
      
if __name__ == '__main__': 
    main()
