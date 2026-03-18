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
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv` or see the official docs).
- Access to Jira API with the necessary permissions.

## Installation
1. Install dependencies using `uv`:
   ```sh
   uv sync
   ```
   This will automatically create a virtual environment and install all dependencies from `pyproject.toml` (or `uv.lock` if present).

2. To add a new dependency:
   ```sh
   uv add <package-name>
   ```

3. To run the script within the managed environment:
   ```sh
   uv run python main.py
   ```

## Docker Build and Push
To build the Docker image for this application and push it to Docker Hub, follow these steps:

1. **Build the Docker image**:
   Use the following command to build the image with a tag. Replace `docker_hub/jira-worklog:1.0` with your desired Docker Hub username and image tag.

   ```sh
   docker build . -t docker_hub/jira-worklog:tag
   ```

2. **Push the image to Docker Hub**:
   After building, push the image to your Docker Hub repository. Ensure you are logged in to your Docker Hub account via the command line.

   ```sh
   docker push docker_hub/jira-worklog:tag
   ```

## Error Handling
- The script will print a message if no logged time is found for the given date range.
- Ensure API credentials and network access to Jira are properly configured.

## License
This project is licensed under the MIT License.

## Contributions
Feel free to open issues or submit pull requests to improve the script.