# Zoom Camera Usage Tracker

This script tracks how long participants keep their cameras off during Zoom meetings. It's designed specifically for recurring meetings, allowing you to track camera usage across multiple sessions.

## Features

- Tracks when participants turn their cameras on and off
- Calculates total camera-off time for each participant
- Maintains cumulative statistics across multiple meeting sessions
- Generates per-session and cumulative reports
- Exports detailed data to CSV files

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Zoom App

1. Go to the [Zoom Marketplace](https://marketplace.zoom.us/) and sign in
2. Click "Develop" → "Build App"
3. Choose "Server-to-Server OAuth" app type
4. Complete the app creation process
5. Under "Scopes", add the following permissions:
   - `meeting:read:participant:admin` (View a meeting's participant)
   - `meeting:read:meeting:admin` (View a meeting)

### 3. Set Up Environment Variables

Create a `.env` file in the same directory as the script with the following content:

```
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_MEETING_ID=your_meeting_id
```

Replace the placeholders with your actual credentials from the Zoom Marketplace app you created.

## Usage

### For a Single Meeting

Run the script at the beginning of your meeting:

```bash
python zoom_camera_tracker.py
```

The script will run for the duration specified (default: 3.5 hours) and generate reports at the end.

### For Recurring Meetings

1. Run the script at the beginning of each meeting session
2. The script will automatically load data from previous sessions
3. After all sessions, you'll have:
   - Individual session reports
   - Cumulative statistics across all sessions
   - A detailed breakdown showing per-day camera usage

## Output Files

The script generates several types of files:

- **Interim files**: Generated every 30 minutes during a meeting
- **Session files**: Show camera usage for a single meeting
- **Cumulative files**: Show total camera usage across all meetings
- **Detailed history file**: Shows day-by-day breakdown for each participant

## Troubleshooting

- **API Rate Limits**: If you encounter rate limiting, increase the `interval_seconds` parameter
- **Missing Data**: Ensure your Zoom account has the correct permissions
- **Authentication Errors**: Verify your credentials in the `.env` file

## Privacy Considerations

This tool only tracks camera status, not audio or content shared during meetings. Be sure to inform participants that you're tracking camera usage for accountability purposes.
