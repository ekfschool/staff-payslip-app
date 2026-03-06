import streamlit as st
import pandas as pd

# --- CONFIG ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSuvLtCwDy7OEtS4zVnH9aVY3f2-WJlU9jetey3Cnmmf_MnZfCb8Lh1Z-sKDilEmEiwJ8JAWZCfhEQQ/pub?output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df

df = load_data()

st.title("Staff Payslip Portal")
st.write("Log in using your Email and Staff ID to view your payslip.")

email_input = st.text_input("Staff Email")
staffid_input = st.text_input("Staff ID", type="password")
login_button = st.button("Login")

if login_button:
    user = df[(df['Staff Email'] == email_input) & (df['Staff ID'] == staffid_input)]
    
    if not user.empty:
        st.success(f"Welcome, {user.iloc[0]['Staff Full Name']}!")
        st.write("**Staff ID:**", user.iloc[0]['Staff ID'])
        st.write("**Gender:**", user.iloc[0]['Gender'])
        st.write("**Grade Level:**", user.iloc[0]['Grade Level'])
        st.subheader("Download Payslip")
        st.markdown(f"[Click here to download your payslip]({user.iloc[0]['Payslip file']})")
    else:

        st.error("Invalid Email or Staff ID. Please try again.")
