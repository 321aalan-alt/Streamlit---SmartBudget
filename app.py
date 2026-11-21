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

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt


# Generate a printable SmartBudget PDF report
def generate_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    pdf.setFillColor(colors.HexColor("#167347"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(45, height - 55, "SmartBudget")

    pdf.setFillColor(colors.HexColor("#152238"))
    pdf.setFont("Helvetica", 11)
    pdf.drawString(45, height - 75, "Monthly Personal Finance Report")

    # Financial summary
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(45, height - 115, "Financial Summary")

    pdf.setFont("Helvetica", 11)
    summary = [
        ("Monthly Income", f"${income:,.2f}"),
        ("Total Expenses", f"${total_expenses:,.2f}"),
        ("Remaining Balance", f"${remaining_balance:,.2f}"),
        ("Savings Rate", f"{savings_rate:.1f}%")
    ]

    y = height - 140
    for label, value in summary:
        pdf.drawString(50, y, label)
        pdf.drawRightString(width - 50, y, value)
        y -= 23

    # Donut chart with percentages inside the slices
    if total_expenses > 0:
        chart_data = expense_data[expense_data["Amount"] > 0]

        fig, ax = plt.subplots(figsize=(6, 4))

        wedges, texts, autotexts = ax.pie(
            chart_data["Amount"],
            autopct="%1.1f%%",
            pctdistance=0.78,
            startangle=90,
            wedgeprops={
                "width": 0.45,
                "edgecolor": "white"
            },
            textprops={
                "fontsize": 10,
                "weight": "bold",
                "color": "black"
            }
        )

        ax.legend(
            wedges,
            chart_data["Category"],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=9
        )

        ax.set_aspect("equal")
        fig.tight_layout()

        chart_buffer = BytesIO()
        fig.savefig(
            chart_buffer,
            format="png",
            dpi=200,
            bbox_inches="tight",
            facecolor="white"
        )
        plt.close(fig)
        chart_buffer.seek(0)

        from reportlab.lib.utils import ImageReader

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(
            45, height - 265,
            "Monthly Spending Breakdown"
        )

        pdf.drawImage(
            ImageReader(chart_buffer),
            45,
            height - 535,
            width=520,
            height=250,
            preserveAspectRatio=True
        )

    # Savings goal
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(45, 210, "Savings Goal")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        50, 185,
        f"Target Savings: ${savings_goal:,.2f}"
    )

    if remaining_balance > 0:
        pdf.drawString(
            50, 165,
            f"Estimated Time: {months_needed} months"
        )
    else:
        pdf.drawString(
            50, 165,
            "No available monthly savings."
        )

    # Footer
    pdf.setStrokeColor(colors.lightgrey)
    pdf.line(45, 75, width - 45, 75)

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(colors.grey)
    pdf.drawCentredString(
        width / 2,
        55,
        "Generated with SmartBudget | Personal Finance Tracker"
    )

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# PDF download button
st.divider()
st.header("Download Your Financial Report")

pdf_data = generate_pdf()

st.download_button(
    label="📄 Download Financial Report (PDF)",
    data=pdf_data,
    file_name="SmartBudget_Financial_Report.pdf",
    mime="application/pdf"
)
