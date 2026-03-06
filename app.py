import streamlit as st
import pandas as pd
import requests
import re

# --- CONFIG ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSuvLtCwDy7OEtS4zVnH9aVY3f2-WJlU9jetey3Cnmmf_MnZfCb8Lh1Z-sKDilEmEiwJ8JAWZCfhEQQ/pub?output=csv"

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df

df = load_data()

# --- APP TITLE ---
st.title("Staff Payslip Portal")
st.write("Log in using your Email and Staff ID to view your payslip.")

# --- LOGIN FORM ---
st.subheader("Login")
email_input = st.text_input("Staff Email")
staffid_input = st.text_input("Staff ID", type="password")
login_button = st.button("Login")

# --- HELPER FUNCTION ---
def convert_to_drive_preview(url):
    """
    Converts a standard Google Drive link to a preview link and a download link.
    """
    match = re.search(r'/d/([a-zA-Z0-9_-]+)/', url)
    if match:
        file_id = match.group(1)
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return preview_url, download_url
    else:
        # fallback if regex fails
        return url, url

# --- LOGIN CHECK ---
if login_button:
    user = df[(df['Staff Email'] == email_input) & (df['Staff ID'] == staffid_input)]
    
    if not user.empty:
        user_row = user.iloc[0]
        
        # --- STAFF DETAILS ---
        st.markdown(f"# {user_row['Staff Full Name']}")
        st.write("**Staff ID:**", user_row['Staff ID'])
        st.write("**Grade Level:**", user_row['Grade Level'])
        st.write("**Gender:**", user_row['Gender'])
        st.write("**Month:**", user_row['Month'])
        
        # --- PDF PREVIEW ---
        if 'Month' in user_row.index:
            st.subheader(f"Payslip Preview - {user_row['Month']}")
        else:
            st.subheader("Payslip Preview")
        
        pdf_original_url = user_row['Payslip file']
        pdf_preview_url, pdf_download_url = convert_to_drive_preview(pdf_original_url)
        
        pdf_display = f'''
        <iframe 
            src="{pdf_preview_url}" 
            width="100%" 
            height="600px" 
            style="border: none;" 
            type="application/pdf">
        </iframe>
        '''
        st.components.v1.html(pdf_display, height=650, scrolling=True)
        
        # --- DOWNLOAD BUTTON ---
        pdf_content = requests.get(pdf_download_url).content
        st.download_button(
            label="Download Payslip",
            data=pdf_content,
            file_name=f"{user_row['Staff Full Name']}_Payslip.pdf",
            mime="application/pdf"
        )
        
    else:
        st.error("Invalid Email or Staff ID. Please try again.")

