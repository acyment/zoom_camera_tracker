from datetime import datetime

class ParticipantTracker:
    def __init__(self):
        self.participants = {}

    def initialize_participant(self, user_id, user_name, current_time):
        """Initialize tracking for a new participant"""
        if user_id not in self.participants:
            self.participants[user_id] = {
                "name": user_name,
                "camera_off_total": 0,
                "cumulative_camera_off_total": 0,
                "camera_off_start": None,
                "join_time": current_time,
                "session_history": []
            }
        elif self.participants[user_id]["join_time"] is None:
            # Returning participant in this session
            self.participants[user_id]["join_time"] = current_time

    def update_camera_status(self, user_id, user_name, video_status, current_time):
        """Update camera status for a participant"""
        if video_status == "off" and self.participants[user_id]["camera_off_start"] is None:
            # Camera just turned off
            print(f"[{current_time.strftime('%H:%M:%S')}] {user_name} turned camera OFF")
            self.participants[user_id]["camera_off_start"] = current_time
        elif video_status == "on" and self.participants[user_id]["camera_off_start"] is not None:
            # Camera just turned on, calculate time it was off
            off_duration = (current_time - self.participants[user_id]["camera_off_start"]).total_seconds()
            self.participants[user_id]["camera_off_total"] += off_duration
            print(f"[{current_time.strftime('%H:%M:%S')}] {user_name} turned camera ON (was off for {off_duration:.1f} seconds)")
            self.participants[user_id]["camera_off_start"] = None
