import requests

class ZoomAPI:
    def __init__(self, auth_manager):
        self.auth_manager = auth_manager

    def get_participants(self, meeting_id):
        """Get current meeting participants"""
        token = self.auth_manager.get_access_token()
        if not token:
            print("Failed to get access token")
            return []

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"https://api.zoom.us/v2/meetings/{meeting_id}/participants"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data.get("participants", [])
            elif response.status_code == 404:
                print(f"Error: Meeting {meeting_id} not found or has ended")
                return []
            elif response.status_code == 401:
                print("Error: Unauthorized. Check your API credentials and scopes")
                print("Required scopes: meeting:read:meeting:admin and meeting:read:participant:admin")
                return []
            else:
                print(f"Error getting participants: {response.status_code}")
                print(response.text)
                return []
        except Exception as e:
            print(f"Exception when calling API: {str(e)}")
            return []
