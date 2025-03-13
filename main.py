import os
import dotenv
import time
from datetime import datetime
from auth.zoom_auth import ZoomAuth
from api.zoom_api import ZoomAPI
from tracking.participant_tracker import ParticipantTracker
from tracking.session_manager import SessionManager
from reporting.report_generator import ReportGenerator

class ZoomCameraTracker:
    def __init__(self, account_id, client_id, client_secret, meeting_id):
        self.auth = ZoomAuth(account_id, client_id, client_secret)
        self.api = ZoomAPI(self.auth)
        self.tracker = ParticipantTracker()
        self.session = SessionManager(meeting_id)
        self.meeting_id = meeting_id

    def track_camera_usage(self, duration_seconds, interval_seconds=10, save_interim=True, interim_minutes=30):
        """Track camera usage for the specified duration"""
        session_day = datetime.now().strftime("%A")
        session_date = datetime.now().strftime("%Y-%m-%d")

        print(f"Starting camera tracking for meeting {self.meeting_id}")
        print(f"Session: {session_day}, {session_date}")
        print(f"Tracking will run for {duration_seconds/60:.1f} minutes")
        print(f"Will check camera status every {interval_seconds} seconds")
        if save_interim:
            print(f"Interim results will be saved every {interim_minutes} minutes")
        print("-" * 50)

        end_time = time.time() + duration_seconds
        last_save_time = time.time()

        while time.time() < end_time:
            current_time = datetime.now()
            participants = self.api.get_participants(self.meeting_id)

            # Log number of participants in this polling interval
            print(f"[{current_time.strftime('%H:%M:%S')}] Found {len(participants)} participants")

            for participant in participants:
                user_id = participant.get("id")
                user_name = participant.get("name")
                video_status = participant.get("video", "off")

                # Initialize participant if new
                self.tracker.initialize_participant(user_id, user_name, current_time)
                
                # Update camera status
                self.tracker.update_camera_status(user_id, user_name, video_status, current_time)

            # Check if we should save interim results
            if save_interim and time.time() - last_save_time > interim_minutes * 60:
                print(f"\n[{current_time.strftime('%H:%M:%S')}] Saving interim results...")
                self.save_interim_results(current_time)
                last_save_time = time.time()

            # Sleep until next interval
            time.sleep(interval_seconds)

        # Final calculations and save data
        self.finalize_session(session_day, session_date)

    def save_interim_results(self, current_time):
        """Save interim results"""
        interim_date_str = current_time.strftime("%Y%m%d_%H%M%S")
        interim_filename = f"interim_zoom_tracking_{self.meeting_id}_{interim_date_str}.csv"
        
        reporter = ReportGenerator(self.tracker.participants)
        reporter.save_session_to_csv(interim_filename)
        self.session.save_cumulative_data()

    def finalize_session(self, session_day, session_date):
        """Finalize the current tracking session"""
        # Update cumulative totals and session history
        for user_id, data in self.tracker.participants.items():
            # Update cumulative total
            data["cumulative_camera_off_total"] += data["camera_off_total"]

            # Add to session history
            if data["join_time"]:
                session_record = {
                    "session_id": self.session.current_session_id,
                    "day": session_day,
                    "date": session_date,
                    "camera_off_seconds": data["camera_off_total"],
                    "camera_off_minutes": round(data["camera_off_total"] / 60, 2)
                }

                if "session_history" not in data:
                    data["session_history"] = []

                data["session_history"].append(session_record)

        # Save final results
        print("-" * 50)
        print("Tracking completed!")

        # Create reporter and save results
        reporter = ReportGenerator(self.tracker.participants)
        
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_filename = f"session_zoom_tracking_{self.meeting_id}_{date_str}.csv"
        cumulative_filename = f"cumulative_zoom_tracking_{self.meeting_id}_{date_str}.csv"

        reporter.save_session_to_csv(session_filename)
        reporter.save_cumulative_to_csv(cumulative_filename)
        self.session.save_cumulative_data()

        # Print results
        reporter.print_session_results(self.meeting_id)
        reporter.print_cumulative_results(self.meeting_id)

if __name__ == "__main__":
    # Load credentials from .env file
    dotenv.load_dotenv()

    # Get credentials from environment variables
    ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
    CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
    CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
    MEETING_ID = os.getenv("ZOOM_MEETING_ID")

    # Validate credentials were loaded properly
    if not all([ACCOUNT_ID, CLIENT_ID, CLIENT_SECRET, MEETING_ID]):
        print("Error: Missing credentials in .env file")
        print("Please create a .env file with the following variables:")
        print("ZOOM_ACCOUNT_ID=your_account_id")
        print("ZOOM_CLIENT_ID=your_client_id")
        print("ZOOM_CLIENT_SECRET=your_client_secret")
        print("ZOOM_MEETING_ID=your_meeting_id")
        exit(1)

    # Create tracker
    tracker = ZoomCameraTracker(
        account_id=ACCOUNT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        meeting_id=MEETING_ID
    )

    # Track for the duration of your meeting (3.5 hours = 12,600 seconds)
    tracker.track_camera_usage(duration_seconds=12600, interval_seconds=15, save_interim=True, interim_minutes=30)
