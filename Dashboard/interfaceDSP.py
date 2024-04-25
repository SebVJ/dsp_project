import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Data
data = pd.read_csv("Ames_Housing_Data.csv")

print(data)
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
#Tool section 1

#Train model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = data[['MS Zoning', 'Lot Area', 'House Style', 'Year Built']]
y = data['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)



"""
st.subheader("Property Price Predictor")

st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")


# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart.
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)   
"""