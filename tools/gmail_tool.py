import os
import json
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_secret(name):
    """
    Get value from Streamlit Secrets if available,
    otherwise get it from environment variables.
    """

    try:
        value = st.secrets.get(name)

        if value:
            return value

    except Exception:
        pass

    return os.getenv(name)


def authenticate_gmail():

    creds = None

    # =====================================================
    # STREAMLIT CLOUD
    # =====================================================

    google_token = get_secret("GOOGLE_TOKEN")

    if google_token:

        try:
            token_data = json.loads(google_token)

            creds = Credentials.from_authorized_user_info(
                token_data,
                SCOPES
            )

        except Exception as e:
            raise RuntimeError(
                f"Could not load GOOGLE_TOKEN: {e}"
            )

    # =====================================================
    # LOCAL
    # =====================================================

    else:

        if os.path.exists("token.json"):

            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

    # =====================================================
    # REFRESH TOKEN
    # =====================================================

    if creds and creds.expired and creds.refresh_token:

        try:
            creds.refresh(Request())

        except Exception as e:
            raise RuntimeError(
                f"Gmail token refresh failed: {e}"
            )

    # =====================================================
    # FIRST TIME LOCAL LOGIN
    # =====================================================

    elif not creds or not creds.valid:

        google_credentials = get_secret("GOOGLE_CREDENTIALS")

        if google_credentials:

            try:
                credentials_data = json.loads(
                    google_credentials
                )

                # Create temporary credentials file
                # only for local authentication if needed

                client_config = credentials_data

                flow = InstalledAppFlow.from_client_config(
                    client_config,
                    SCOPES
                )

                creds = flow.run_local_server(
                    port=0
                )

            except Exception as e:
                raise RuntimeError(
                    f"Gmail OAuth authentication failed: {e}"
                )

        else:

            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json not found."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        # Save token only locally
        if not google_token:

            with open("token.json", "w") as token:
                token.write(
                    creds.to_json()
                )

    # =====================================================
    # BUILD GMAIL SERVICE
    # =====================================================

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service