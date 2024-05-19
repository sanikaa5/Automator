# Email Task Automator

This project automates various email tasks using the Gmail API.

## Setup

1. **Obtain OAuth 2.0 Credentials**:
   - Go to the [Google Cloud Console] (https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API for your project.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.

2. **Project Structure**:
   - Place the `credentials.json` file obtained from the Google Cloud Console in the project directory.
   - Place the provided Python script files (`email_send.py`, `email_reply.py`, `email_sort.py`) in the project directory.

3. **Installing Dependencies**:
   - Install the required Python libraries using pip:
     ```bash
     pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
     ```

## Usage

1. **email_sort.py**:
   - This script searches for specific subjects in emails and retrieves their content.

2. **email_send.py**:
   - This script sends an email to multiple recipients with a message and a link to a Google Sheets document.

3. **email_reply.py**:
   - This script automatically replies to emails with a specific subject keyword.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

## License

This project is licensed under the MIT License.

