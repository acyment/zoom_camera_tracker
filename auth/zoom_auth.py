import time
import base64
import requests

class ZoomAuth:
    def __init__(self, account_id, client_id, client_secret):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0

    def get_access_token(self):
        """Get OAuth access token using Server-to-Server OAuth flow"""
        # If token is still valid, reuse it
        current_time = time.time()
        if self.access_token and current_time < self.token_expiry:
            return self.access_token

        # Token is expired or doesn't exist, get a new one
        token_url = "https://zoom.us/oauth/token"
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id
        }

        response = requests.post(token_url, headers=headers, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            # Set token expiry time (usually 1 hour minus 5 minutes buffer)
            self.token_expiry = current_time + token_data.get("expires_in", 3600) - 300
            return self.access_token
        else:
            print(f"Error getting access token: {response.status_code}")
            print(response.text)
            return None
