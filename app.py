import streamlit as st
import pandas as pd
import requests
import re

# --- CONFIG ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSuvLtCwDy7OEtS4zVnH9aVY3f2-WJlU9jetey3Cnmmf_MnZfCb8Lh1Z-sKDilEmEiwJ8JAWZCfhEQQ/pub?output=csv"

# Load data from Google Sheet
@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    return df

df = load_data()

st.title("Staff Payslip Portal")
st.write("Log in using your Email and Staff ID to view your payslip.")

# --- LOGIN ---
st.subheader("Login")
email_input = st.text_input("Staff Email")
staffid_input = st.text_input("Staff ID", type="password")
login_button = st.button("Login")

def convert_to_drive_preview(url):
    """
    Convert a standard Google Drive link to a preview link and get file ID.
    Works with links like:
    https://drive.google.com/file/d/FILE_ID/view?usp=sharing
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

if login_button:
    user = df[(df['Staff Email'] == email_input) & (df['Staff ID'] == staffid_input)]
    
    if not user.empty:
        # Display Full Name as large header
        st.markdown(f"# {user.iloc[0]['Staff Full Name']}")
        
        # Display other details
        st.write("**Staff ID:**", user.iloc[0]['Staff ID'])
        st.write("**Gender:**", user.iloc[0]['Gender'])
        st.write("**Grade Level:**", user.iloc[0]['Grade Level'])
        
        # Get preview and download URLs
        pdf_original_url = user.iloc[0]['Payslip file']
        pdf_preview_url, pdf_download_url = convert_to_drive_preview(pdf_original_url)
        
        # Display PDF preview (mobile-friendly)
        st.subheader("Payslip Preview")
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
        
        # Download button
        pdf_content = requests.get(pdf_download_url).content
        st.download_button(
            label="Download Payslip",
            data=pdf_content,
            file_name=f"{user.iloc[0]['Staff Full Name']}_Payslip.pdf",
            mime="application/pdf"
        )
        
    else:
        st.error("Invalid Email or Staff ID. Please try again.")
