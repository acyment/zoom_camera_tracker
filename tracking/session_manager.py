import pickle
import os
from datetime import datetime

class SessionManager:
    def __init__(self, meeting_id):
        self.meeting_id = meeting_id
        self.current_session_start = datetime.now()
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.cumulative_data_file = f"zoom_cumulative_data_{meeting_id}.pkl"
        self.participants = {}

    def load_cumulative_data(self):
        """Load previous tracking data if available"""
        if os.path.exists(self.cumulative_data_file):
            try:
                with open(self.cumulative_data_file, 'rb') as f:
                    self.participants = pickle.load(f)
                print(f"Loaded cumulative data for {len(self.participants)} participants from previous sessions")

                # Initialize new session data
                for user_id in self.participants:
                    # Keep cumulative_camera_off_total but reset session-specific values
                    if 'cumulative_camera_off_total' not in self.participants[user_id]:
                        self.participants[user_id]['cumulative_camera_off_total'] = self.participants[user_id].get('camera_off_total', 0)

                    # Reset session-specific tracking
                    self.participants[user_id]['camera_off_total'] = 0
                    self.participants[user_id]['camera_off_start'] = None
                    self.participants[user_id]['join_time'] = None

                    # Add session history if not present
                    if 'session_history' not in self.participants[user_id]:
                        self.participants[user_id]['session_history'] = []
            except Exception as e:
                print(f"Error loading cumulative data: {e}")
                print("Starting with fresh tracking data")

    def save_cumulative_data(self):
        """Save cumulative tracking data for future sessions"""
        try:
            with open(self.cumulative_data_file, 'wb') as f:
                pickle.dump(self.participants, f)
            print(f"Saved cumulative data to {self.cumulative_data_file}")
        except Exception as e:
            print(f"Error saving cumulative data: {e}")
