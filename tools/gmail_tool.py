import json
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]
print(type(st.secrets["GOOGLE_TOKEN"]))

json.loads(
    st.secrets["GOOGLE_TOKEN"]
)

print("JSON loaded successfully")

def authenticate_gmail():

    token_info = json.loads(
        st.secrets["GOOGLE_TOKEN"]
    )

    creds = Credentials.from_authorized_user_info(
        token_info,
        SCOPES
    )

    if creds.expired and creds.refresh_token:

        creds.refresh(
            Request()
        )

    service = build(

        "gmail",

        "v1",

        credentials=creds

    )

    return service