import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold


df = pd.read_excel('/Users/andreasbrogaard/Documents/dsp_project/dsp_project/Data Collection/gpt_response_clean.xlsx')
df = df[['Type', 'Ask.price', 'Year_built', 'Energy_rating', 'Monthly_ownership_cost', 'Days_desc', 'Municipality', 'Rooms', 'Location', '#Bathrooms', 'Cond.house', 'View', 'Balcony', 'Garden', 'Parking', 'Swimming pool', 'Fireplace', 'Garage', 'Basement', 'Elevator', 'Air_conditioning', 'Heating_type']]


#### Dropping NA values ####
df.dropna(inplace=True)


#Converting data types
df['Ask.price'] = pd.to_numeric(df['Ask.price'], errors='coerce')
df['Monthly_ownership_cost'] = pd.to_numeric(df['Monthly_ownership_cost'], errors='coerce')
df['Days_desc'] = df['Days_desc'].astype('category')
df['Municipality'] = df['Municipality'].astype('category')
df['Year_built'] = df['Year_built'].astype(int)
df['Rooms'] = df['Rooms'].astype(int)
df['Energy_rating'] = df['Energy_rating'].astype('category')
df['Location'] = df['Location'].astype('category')
df['#Bathrooms'] = df['#Bathrooms'].astype('category')
df['cond.house'] = df['Cond.house'].astype('category')
df['View'] = df['View'].astype('category')

#### Removing Zero and Near Zero variance features ####

# Set the threshold for variance
threshold = 0.01

# Create the VarianceThreshold object
selector = VarianceThreshold(threshold=threshold)

df_encoded = pd.get_dummies(df)

# Fit the selector to the data
selector.fit(df_encoded)

# Get the indices of the selected features
selected_indices = selector.get_support(indices=True)

# Filter the dataframe based on the selected indices
df_filtered = df_encoded.iloc[:, selected_indices]


#### Log transformation of 'Ask.price' and 'Monthly_ownership_cost' columns ####

# Log transformation function
def log_transform(x):
    return np.log(x)

# Apply log transformation to 'Ask.price' and 'Monthly_ownership_cost' columns
df_filtered['Ask.price_log'] = df_filtered['Ask.price'].apply(log_transform)
df_filtered['Monthly_ownership_cost_log'] = df_filtered['Monthly_ownership_cost'].apply(log_transform)

# Drop the original 'Ask.price' and 'Monthly_ownership_cost' columns
df_filtered.drop(['Ask.price', 'Monthly_ownership_cost'], axis=1, inplace=True)

# Save the filtered dataframe to a CSV file
df_filtered.to_pickle('/Users/andreasbrogaard/Documents/dsp_project/dsp_project/2. Feature engineering/housing_data_engineered.pkl')
