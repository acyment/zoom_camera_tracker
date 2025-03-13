import csv
from datetime import datetime

class ReportGenerator:
    def __init__(self, participants):
        self.participants = participants

    def get_session_results(self):
        """Get results for the current session"""
        results = []
        for user_id, data in self.participants.items():
            # Skip if they didn't join this session
            if data["join_time"] is None:
                continue

            total_seconds = data["camera_off_total"]

            # Calculate total time in meeting
            total_time = (datetime.now() - data["join_time"]).total_seconds()
            percentage = (total_seconds / total_time * 100) if total_time > 0 else 0

            results.append({
                "name": data["name"],
                "camera_off_seconds": total_seconds,
                "camera_off_minutes": round(total_seconds / 60, 2),
                "percentage_off": round(percentage, 2),
                "join_time": data["join_time"]
            })
        return results

    def get_cumulative_results(self):
        """Get cumulative results across all sessions"""
        results = []
        for user_id, data in self.participants.items():
            total_seconds = data["cumulative_camera_off_total"]

            # Count number of sessions this person attended
            attended_sessions = len(data.get("session_history", []))

            results.append({
                "name": data["name"],
                "camera_off_seconds": total_seconds,
                "camera_off_minutes": round(total_seconds / 60, 2),
                "attended_sessions": attended_sessions
            })
        return results

    def print_session_results(self, meeting_id):
        """Print the results for current session to console"""
        results = self.get_session_results()

        # Sort by camera off time (descending)
        sorted_results = sorted(results, key=lambda x: x["camera_off_seconds"], reverse=True)

        print("\n===== CAMERA USAGE RESULTS (THIS SESSION) =====")
        print(f"Meeting ID: {meeting_id}")
        print(f"Session Date: {datetime.now().strftime('%Y-%m-%d (%A)')}")
        print(f"Total Participants: {len(sorted_results)}")
        print("-" * 80)
        print(f"{'Participant Name':<30} {'Camera Off Time':<15} {'Percentage Off':<20}")
        print("-" * 80)

        for result in sorted_results:
            name = result["name"]
            off_minutes = result["camera_off_minutes"]
            percentage = result["percentage_off"]

            print(f"{name[:30]:<30} {off_minutes:>5.2f} min     {percentage:>6.2f}%")

        print("-" * 80)

    def print_cumulative_results(self, meeting_id):
        """Print the cumulative results across all sessions"""
        results = self.get_cumulative_results()

        # Sort by camera off time (descending)
        sorted_results = sorted(results, key=lambda x: x["camera_off_seconds"], reverse=True)

        print("\n===== CUMULATIVE CAMERA USAGE RESULTS =====")
        print(f"Meeting ID: {meeting_id}")
        print(f"Total Tracked Participants: {len(sorted_results)}")
        print("-" * 80)
        print(f"{'Participant Name':<30} {'Total Camera Off Time':<20} {'Sessions Attended':<20}")
        print("-" * 80)

        for result in sorted_results:
            name = result["name"]
            off_minutes = result["camera_off_minutes"]
            sessions = result["attended_sessions"]

            print(f"{name[:30]:<30} {off_minutes:>7.2f} min     {sessions:>3}")

        print("-" * 80)

    def save_session_to_csv(self, filename):
        """Save current session results to a CSV file"""
        results = self.get_session_results()

        # Sort by camera off time (descending)
        sorted_results = sorted(results, key=lambda x: x["camera_off_seconds"], reverse=True)

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'camera_off_seconds', 'camera_off_minutes', 'percentage_off', 'join_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in sorted_results:
                writer.writerow(result)

        print(f"Session results saved to {filename}")

    def save_cumulative_to_csv(self, filename):
        """Save cumulative results to a CSV file"""
        results = self.get_cumulative_results()

        # Sort by camera off time (descending)
        sorted_results = sorted(results, key=lambda x: x["camera_off_seconds"], reverse=True)

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'camera_off_seconds', 'camera_off_minutes', 'attended_sessions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for result in sorted_results:
                writer.writerow(result)

        print(f"Cumulative results saved to {filename}")

    def save_detailed_history_to_csv(self, filename=None):
        """Save detailed session history for all participants"""
        if filename is None:
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detailed_history_{self.meeting_id}_{date_str}.csv"

        # Flatten the data for CSV export
        flat_data = []
        for user_id, data in self.participants.items():
            name = data["name"]
            for session in data.get("session_history", []):
                flat_data.append({
                    "name": name,
                    "session_id": session.get("session_id", ""),
                    "day": session.get("day", ""),
                    "date": session.get("date", ""),
                    "camera_off_seconds": session.get("camera_off_seconds", 0),
                    "camera_off_minutes": session.get("camera_off_minutes", 0)
                })

        # Sort by name and date
        sorted_data = sorted(flat_data, key=lambda x: (x["name"], x["date"]))

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'session_id', 'day', 'date', 'camera_off_seconds', 'camera_off_minutes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in sorted_data:
                writer.writerow(row)

        print(f"Detailed history saved to {filename}")
