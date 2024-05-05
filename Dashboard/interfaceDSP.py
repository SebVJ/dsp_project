import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
print(os.getcwd())
os.chdir('C:/Users/MadsN/Desktop/DSP_project/dsp_project/Dashboard')

#Data
data = pd.read_csv("Ames_Housing_Data.csv")


#Standard website config.
st.set_page_config(page_title="Data Science Project", page_icon=":tada:", layout = "wide")

# Header section
with st.container():
    st.subheader("Data Science Project, Spring 2024")
    st.title("Property Price Predictor")
    st.write("The following is a tool which will help you predict the market price of a property.") 
    st.write("The tool requires property specifications as input which it then can use for price predictions by comparing properties of similar specifications.")


#Intro section 1
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("How to use")
        st.write("##")
        st.write(
            """
            The price of the property is build on the following specifications which you will need to provide:
            - Location
            - Square meters
            - Year of construction
            - Anything else which is useful
            """
        )
        st.write("[Data sourced from >](https://edc.dk)")
    with right_column:
        st.write("# Specifications")
        
        st.write(data)

#Intro section 2
with st.container():
    st.subheader("Historic property prices in Aarhus Kommune")
    data_to_plot = data[['SalePrice']]
    st.line_chart(data=data_to_plot)
#__________________________________________________________________________
#Training the model

### Train model ####
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data.info() #we have two 'object' variables (which we'll later OneHot encode)

#Removing small categories and converting 'Year Built' to 'Age'
data = data[data['House Style'] != '2.5Fin']#Running this for categories in variables that have a low count
data = data[data['House Style'] != '1.5Unf']
data = data[data['House Style'] != '2.5Unf'] 
data = data[data['MS Zoning'] != 'RH'] 
print(data['House Style'].value_counts()) #Counting category occurences.

data['Age'] = 2024 - data['Year Built'] #Converting variable
data = data.drop(columns=['Year Built'])#Removing old variable

## Data and feature engineering ##
X = data[['Lot Area', 'Age']]
y = data['SalePrice']

#OneHot encoding
#X = pd.get_dummies(X, columns=['House Style', 'MS Zoning'])

X.info()

#Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import mean_squared_error
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(rmse)
import statistics
dev = rmse/statistics.mean(y)
print(dev) 
#______________________________________________________________________________________________________________
#Implement tool in interface

import joblib as jb
#Save model to file
jb.dump(model, 'house_price_prediction_model.pkl')

#Load the trained model
model = jb.load('house_price_prediction_model.pkl')

#Title of dashboard
st.title('Property Price Pedictor')


#house_styles = ['House Style_1.5Fin', 'House Style_1Story', 'House Style_2Story', 'House Style_SFoyer', 'House Style_SLvl']
#ms_zoning = ['MS Zoning_A (agr)', 'MS Zoning_C (all)', 'MS Zoning_FV', 'MS Zoning_I (all)', 'MS Zoning_RL', 'MS Zoning_RM']

# Input fields for the user to enter data
lot_area = st.number_input('Lot Area', min_value=1000, max_value=20000, value=5000, step=100)
age = st.slider('Age', 0, 100, 10)

# Predict button
if st.button('Predict Price'):
    # Create the input DataFrame based on the inputs
    input_data = pd.DataFrame({
        'Lot Area': [lot_area],
        'Age': [age]      
    })

    
# Ensure that all columns from the training dataset are present
# Fill missing columns with zeros

    train_columns = model.feature_names_in_  # Replace with actual training columns if needed
    for col in train_columns:
        if col not in input_data.columns:
            input_data[col] = 0
          
    # Predict the price using the model
    prediction = model.predict(input_data)
    
    # Display the prediction
    st.write(f'Predicted Sale Price: ${prediction[0]:,.2f}')

# Optional: You might want to display the RMSE or other performance metrics
st.write('Model RMSE:', rmse)