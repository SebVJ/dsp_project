import pandas as pd
from sklearn.feature_selection import VarianceThreshold
import numpy as np

df = pd.read_excel('/Users/andreasbrogaard/Documents/dsp_project/dsp_project/Data Collection/gpt_response_clean copy.xlsx')
categorical_columns = ['Type', 'Energy_rating', 'Days_desc', 'Municipality', '#Bathrooms', 'Cond.house', 'View', 'Heating_type']


df.drop(['Description'], axis=1, inplace=True)
df.drop(df.columns[0], axis=1, inplace=True)


df_cleaned = df.dropna()


# Apply log transformation to 'Ask.price' and 'Monthly_ownership_cost' columns
df_cleaned['Ask.price_log'] = np.log(df_cleaned['Ask.price'])
df_cleaned['Monthly_ownership_cost_log'] = np.log(df_cleaned['Monthly_ownership_cost'])

# Drop the original 'Ask.price' and 'Monthly_ownership_cost' columns
df_cleaned.drop(['Ask.price', 'Monthly_ownership_cost'], axis=1, inplace=True)


# Extract age of property before encoding 'Municipality'
current_year = 2024
df_cleaned['Age_of_Property'] = current_year - df_cleaned['Year_built']

# Group less frequent municipalities into 'Other'
municipality_counts = df_cleaned['Municipality'].value_counts()
rare_municipalities = municipality_counts[municipality_counts < 5].index
df_cleaned['Municipality'] = df_cleaned['Municipality'].replace(rare_municipalities, 'Other')

# One-hot encode categorical variables including the modified 'Municipality'
df_encoded = pd.get_dummies(df_cleaned, columns=categorical_columns + ['Municipality'], drop_first=True)


df_cleaned.columns = df.columns.astype(str)

#### Removing Zero and Near Zero variance features ####

# Set the threshold for variance
threshold = 0.01

# Create the VarianceThreshold object
selector = VarianceThreshold(threshold=threshold)

# Fit the selector to the data
selector.fit(df_cleaned)

# Get the indices of the selected features
selected_indices = selector.get_support(indices=True)

# Filter the dataframe based on the selected indices
df_filtered = df_cleaned.iloc[:, selected_indices]






# Save the filtered dataframe to a CSV file
df_filtered.to_pickle('/Users/andreasbrogaard/Documents/dsp_project/dsp_project/2. Feature engineering/housing_data_feature_engineered.pkl')
