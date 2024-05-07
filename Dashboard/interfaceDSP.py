import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib as jb
print(os.getcwd())
os.chdir('C:/Users/MadsN/Desktop/DSP_project/dsp_project/Dashboard')

#Data
data_path = 'housing_data_engineered.pkl'
data = jb.load(data_path)
data.info()

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
    data_to_plot = data[['Ask.price_log']]
    st.line_chart(data=data_to_plot)
#__________________________________________________________________________

#Loading the model
model_path = 'Full_Random_Forest_Reg.pkl'
model = jb.load(model_path)


#Check model type and parameters
print(type(model))
print(model.feature_names_in_)
print("Number of Trees:", model.n_estimators)
print("Max Depth:", model.max_depth)
print("Features Importances:", model.feature_importances_)
#__________________________________________________________________________________________________
#Implement tool in interface

#Title of dashboard
st.title('Property Price Pedictor')

data.info()

#### Input fields for the user to enter data ####
#Numeric inputs
year_built = st.number_input('Year built', min_value=1850, max_value=2023, value=2000, step=1)
nrooms = st.slider('Number of Rooms', 1, 6, 1)
#Boolean input
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    balcony = st.checkbox('Balcony')
with col2:
    garden = st.checkbox("Garden")
with col3:
    parking = st.checkbox("Parking")
with col4:
    fireplace = st.checkbox("Fireplace")
with col5:
    garage = st.checkbox("Garage")
with col6:
    basement = st.checkbox("Basement")
with col7:
    elevator = st.checkbox("Elevator")
#Categorical input
type = st.selectbox('Select House Type', ('Andelsbolig', 'Ejerlejlighed', 'Landejendom', 'Rækkehus', 'Villa'))
energy_rating = st.selectbox('Select Energy Rating', ('A2010', 'A2015', 'B', 'C', 'D', 'E', 'G'))
days_for_sale = st.selectbox('Number of days for sale', ('1-10', '100+', '11-20', '21-50', '51-100'))
municipality = st.selectbox('Municipality', ('Aarhus C', 'Aarhus N', 'Aarhus V', 'Brabrand', 'Egå', 'Harlev J', 'Hasselager', 'Hjortshøj', 'Højbjerg', 'Lystrup', 'Malling', 'Risskov', 'Skødstrup', 'Solbjerg', 'Tilst', 'Tranbjerg J', 'Trige', 'Viby J'))
location = st.selectbox('Location', ('central', 'downtown', 'rural', 'suburban', 'urban'))
nbathrooms = st.selectbox('Number of bathrooms',('1', '1-1.5 bathrooms', '2-2.5 bathrooms', '3+ bathrooms', 'not_stated'))
#Condition of house appears twice in dataset
cond_house = st.selectbox('Condition of house', ('fixer-upper', 'new construction', 'not_stated', 'renovated', 'well-maintained'))
view = st.selectbox('View',('city', 'no view', 'not_stated', 'sea'))
#Heating type has recurring variables
heating_type = st.selectbox('Type of heating',('Gulvvarme', 'Radiators', 'Var­me­gen­vin­dings­an­læg', 'fjernvarme', 'floor Heating', 'not_stated'))

# Predict button
if st.button('Predict Price'):
    # Create the input DataFrame based on the inputs
    input_data = pd.DataFrame({
        'Year_built': [year_built],
        'Rooms': [nrooms],
        'Balcony': [balcony], 'Garden': [garden],
        'Parking': [parking],
        'Fireplace': [fireplace],
        'Garage': [garage],
        'Basement': [basement],
        'Elevator': [elevator],
        #Type dropdown menu
        'Type_Andelsbolig': False,
        'Type_Ejerlejlighed': False,
        'Type_Landejendom': False,
        'Type_Rækkehus': False,
        'Type_Villa': False,
        #Energy rating dropdown menu
        'Energy_rating_A2010': False,
        'Energy_rating_A2015': False,
        'Energy_rating_B': False,
        'Energy_rating_C': False,
        'Energy_rating_D': False,
        'Energy_rating_E': False,
        'Energy_rating_G': False,        
        #Days to sell dropdown menu
        'Days_desc_1-10': False,
        'Days_desc_100+': False,
        'Days_desc_11-20': False,
        'Days_desc_21-50': False,
        'Days_desc_51-100': False,
        #Municipality dropdown menu
        'Municipality_Aarhus C': False,
        'Municipality_Aarhus N': False,
        'Municipality_Aarhus V': False,
        'Municipality_Brabrand': False,
        'Municipality_Egå': False,
        'Municipality_Harlev J': False,
        'Municipality_Hasselager': False,
        'Municipality_Hjortshøj': False,
        'Municipality_Højbjerg': False,
        'Municipality_Lystrup': False,
        'Municipality_Malling': False,
        'Municipality_Risskov': False,
        'Municipality_Skødstrup': False,
        'Municipality_Solbjerg': False,
        'Municipality_Tilst': False,
        'Municipality_Tranbjerg J': False,
        'Municipality_Trige': False,
        'Municipality_Viby J': False,     
        #Location dropdown menu
        'Location_central': False, 
        'Location_downtown': False,
        'Location_rural': False,
        'Location_suburban': False,
        'Location_urban': False,
        #Number of bathrooms dropdown menu
        '#Bathrooms_1': False,
        '#Bathrooms_1-1.5 bathrooms': False,
        '#Bathrooms_2-2.5 bathrooms': False,
        '#Bathrooms_3+ bathrooms': False,
        '#Bathrooms_not_stated': False,
        #Condition of house dropdown menu
        'Cond.house_fixer-upper': False,
        'Cond.house_new construction': False,
        'Cond.house_not_stated': False,
        'Cond.house_renovated': False,
        'Cond.house_well-maintained': False,
        #View dropdown menu
        'View_city': False,
        'View_no view': False,
        'View_not_stated': False,
        'View_sea': False,
        #Heating type dropdown menu
        'Heating_type_Gulvvarme': False,
        'Heating_type_Radiators': False,
        'Heating_type_Var­me­gen­vin­dings­an­læg': False,
        'Heating_type_fjernvarme': False,
        'Heating_type_floor heating': False,
        'Heating_type_not_stated': False
        #Condition of house appears twice??
        #Monthly ownership cost??
    })
    input_data[f'Type_{type}'] = True
    input_data[f'Energy_rating_{energy_rating}'] = True
    input_data[f'Days_desc_{days_for_sale}'] = True
    input_data[f'Municipality_{municipality}'] = True
    input_data[f'Location_{location}'] = True
    input_data[f'#Bathrooms_{nbathrooms}'] = True
    input_data[f'Cond.house_{cond_house}'] = True
    input_data[f'View_{view}'] = True
    input_data[f'Heating_type_{heating_type}'] = True



# Ensure that all columns from the training dataset are present
# Fill missing columns with zeros

    train_columns = model.feature_names_in_  # Replace with actual training columns if needed
    for col in train_columns:
        if col not in input_data.columns:
            input_data[col] = 0
          
    # Predict the price using the model
    prediction = model.predict(input_data)
    
    # Display the prediction
    st.write(f'Predicted Sales Price: DKK {prediction[0]:,.2f}')