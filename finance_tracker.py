import streamlit as st
import pandas as pd
from datetime import date
import os

# File to store data
FILE_NAME = "finance_data.csv"

# Page Title
st.title("💰 Personal Finance Tracker")

# Load existing data or create new DataFrame
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount", "Description"])

# Sidebar for adding transaction
st.sidebar.header("Add Transaction")

trans_date = st.sidebar.date_input("Date", date.today())
trans_type = st.sidebar.selectbox("Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category (e.g., Salary, Food, Rent)")
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add"):
    new_data = {
        "Date": trans_date,
        "Type": trans_type,
        "Category": category,
        "Amount": amount,
        "Description": description
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    st.sidebar.success("Transaction Added!")

# Main Section
st.subheader("Transaction History")
st.dataframe(df, use_container_width=True)

# Calculate totals
if not df.empty:
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹ {income:.2f}")
    col2.metric("Total Expense", f"₹ {expense:.2f}")
    col3.metric("Balance", f"₹ {balance:.2f}")

# Download option
st.download_button(
    label="Download Data as CSV",
    data=df.to_csv(index=False),
    file_name="finance_data.csv",
    mime="text/csv"
)