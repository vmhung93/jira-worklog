# Jira Worklog Extractor

## Overview
This script retrieves and displays the time logged in Jira within a specified date range. It fetches issues assigned to the current user, extracts worklogs, and calculates the total time spent on tasks.

## Features
- Fetches Jira issues within the given date range.
- Extracts and filters worklogs for the current user.
- Calculates and displays logged time in hours.
- Provides a detailed breakdown of time spent per issue.
- Displays a summary of total logged hours.

## Prerequisites
Before running the script, ensure you have:
- Python installed (>= 3.7 recommended).
- Access to Jira API with the necessary permissions.
- Installed required dependencies (if applicable).

## Installation
1. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```
2. Install dependencies (if any are required):
   ```sh
   pip install -r requirements.txt
   ```

## Error Handling
- The script will print a message if no logged time is found for the given date range.
- Ensure API credentials and network access to Jira are properly configured.

## License
This project is licensed under the MIT License.

## Contributions
Feel free to open issues or submit pull requests to improve the script.

