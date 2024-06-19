import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Set the title of the Streamlit app
st.title("Mortgage Repayments Calculator")

# Create input fields for user to input mortgage details
st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)  # Home value input
deposit = col1.number_input("Deposit", min_value=0, value=100000)  # Deposit input
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)  # Interest rate input
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)  # Loan term input

# Calculate the mortgage repayments
loan_amount = home_value - deposit  # Calculate loan amount
monthly_interest_rate = (interest_rate / 100) / 12  # Convert annual interest rate to monthly
number_of_payments = loan_term * 12  # Calculate total number of monthly payments
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)  # Calculate monthly payment using the formula for an amortizing loan

# Calculate total repayments and total interest
total_payments = monthly_payment * number_of_payments  # Total amount paid over the loan term
total_interest = total_payments - loan_amount  # Total interest paid over the loan term

# Display the repayment details
st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")  # Monthly repayment amount
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")  # Total repayment amount
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")  # Total interest amount

# Create a data frame with the payment schedule
schedule = []
remaining_balance = loan_amount  # Initialize remaining balance with the loan amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate  # Interest payment for the current month
    principal_payment = monthly_payment - interest_payment  # Principal payment for the current month
    remaining_balance -= principal_payment  # Update the remaining balance
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
    )  # Append payment details for the current month to the schedule

# Convert the schedule to a pandas DataFrame
df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the payment schedule as a chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()  # Group by year and get minimum remaining balance
st.line_chart(payments_df)  # Display the line chart of the payment schedule
