import streamlit as st

st.set_page_config(
    page_title="SmartBudget",
    page_icon="💰",
    layout="wide"
)

st.title("💰 SmartBudget")
st.subheader("Personal Finance Tracker")

st.write("Welcome to SmartBudget! Your personal finance dashboard to track income, expenses, and savings goals.")

st.divider()

st.header("Monthly Income")

income = st.number_input(
    "Enter your monthly income ($)",
    min_value=0.0,
    value=4500.0,
    step=100.0
)

st.metric(
    label="Total Monthly Income",
    value=f"${income:,.2f}"
)

st.divider()

st.header("Monthly Expenses")

housing = st.number_input(
    "Housing / Rent ($)",
    min_value=0.0,
    value=1300.0
)

food = st.number_input(
    "Groceries / Food ($)",
    min_value=0.0,
    value=500.0
)

transportation = st.number_input(
    "Transportation ($)",
    min_value=0.0,
    value=350.0
)

utilities = st.number_input(
    "Utilities ($)",
    min_value=0.0,
    value=250.0
)

other = st.number_input(
    "Other Expenses ($)",
    min_value=0.0,
    value=200.0
)

total_expenses = (
    housing + food + transportation + utilities + other
)

st.metric(
    label="Total Monthly Expenses",
    value=f"${total_expenses:,.2f}"
)

st.divider()

st.header("Financial Summary")

# Calculate remaining balance
remaining_balance = income - total_expenses

# Calculate savings rate
if income > 0:
    savings_rate = (remaining_balance / income) * 100
else:
    savings_rate = 0

# Display financial metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Monthly Income",
        f"${income:,.2f}"
    )

with col2:
    st.metric(
        "Total Expenses",
        f"${total_expenses:,.2f}"
    )

with col3:
    st.metric(
        "Remaining Balance",
        f"${remaining_balance:,.2f}"
    )

st.metric(
    "Savings Rate",
    f"{savings_rate:.1f}%"
)

# Display financial feedback
if remaining_balance > 0:
    st.success("Great! You're spending less than you earn.")
elif remaining_balance == 0:
    st.warning("Your expenses equal your income.")
else:
    st.error("Your expenses exceed your income.")

st.divider()

st.header("Monthly Spending Breakdown")

import pandas as pd
import plotly.express as px

# Organize expenses into a dataset
expense_data = pd.DataFrame({
    "Category": [
        "Housing",
        "Food",
        "Transportation",
        "Utilities",
        "Other"
    ],
    "Amount": [
        housing,
        food,
        transportation,
        utilities,
        other
    ]
})

# Create interactive pie chart
if total_expenses > 0:
    fig = px.pie(
        expense_data,
        names="Category",
        values="Amount",
        title="Where Does Your Money Go?",
        hole=0.4
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#152238"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Enter your expenses to see the chart.")

# Display expense data table
st.subheader("Expense Details")
st.dataframe(expense_data, use_container_width=True)

import math

st.divider()

st.header("🎯 Savings Goal Calculator")

savings_goal = st.slider(
    "Select your savings goal ($)",
    min_value=500,
    max_value=50000,
    value=5000,
    step=500
)

if remaining_balance > 0:
    months_needed = math.ceil(
        savings_goal / remaining_balance
    )

    st.success(
        f"At your current savings rate, you could "
        f"reach your ${savings_goal:,.0f} savings goal "
        f"in approximately {months_needed} months!"
    )

    progress = min(
        remaining_balance / savings_goal, 1.0
    )

    st.progress(progress)

    st.caption(
        "The progress bar shows how much one month's "
        "remaining balance contributes to your goal."
    )

else:
    st.warning(
        "You need a positive remaining balance "
        "to start saving toward your goal."
    )
