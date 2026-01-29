# Gmail Quickstart - LinkedIn Job Alert Parser

A Python application that uses the Gmail API to read LinkedIn Job Alert emails and parse them into structured JSON format using Pydantic models.

## Features

- OAuth2 authentication with Google Gmail API
- Fetch unread LinkedIn Job Alert emails
- Parse job listings from email body (title, company, location, URL)
- Structured JSON output using Pydantic models
- Handles multipart email formats (plain text and HTML)
- Clean URLs with tracking parameters removed

## Requirements

- Python 3.12+
- Google Cloud project with Gmail API enabled
- OAuth 2.0 credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gmail_quickstart
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

   Or add dependencies individually:
   ```bash
   uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib pydantic beautifulsoup4
   ```

   Or with pip:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pydantic beautifulsoup4
   ```

## Google Cloud Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to **APIs & Services > Library**
   - Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to **APIs & Services > Credentials**
   - Click **Create Credentials > OAuth client ID**
   - Select **Desktop app** as the application type
   - Download the credentials and save as `credentials.json` in the project root

## Usage

Run the LinkedIn Job Alert parser:

```bash
uv run readgmail.py
```

Or with Python directly:

```bash
python readgmail.py
```

On first run, a browser window will open for Google authentication. After granting permissions, a `token.json` file will be created to store your credentials for future runs.

## Example Output

The application outputs structured JSON for each LinkedIn Job Alert email:

```json
{
  "id": "19c05dcea1a2afd7",
  "subject": "Your job alert for Director of Engineering in United States",
  "sender": "LinkedIn Job Alerts <jobalerts-noreply@linkedin.com>",
  "date": "Sun, 26 Jan 2026 10:00:00 -0800",
  "snippet": "New jobs match your preferences...",
  "jobs": [
    {
      "title": "Senior Director of Engineering",
      "company": "ClickUp",
      "location": "United States",
      "url": "https://www.linkedin.com/comm/jobs/view/4343659841"
    },
    {
      "title": "Director, Software Engineering",
      "company": "GoodLeap",
      "location": "San Francisco, CA",
      "url": "https://www.linkedin.com/comm/jobs/view/4366287547"
    }
  ]
}
```

## Project Structure

```
gmail_quickstart/
├── models/
│   └── linkedin.py      # Pydantic models (Job, LinkedInJobAlert)
├── readgmail.py         # Main GmailClient class
├── quickstart.py        # Original Gmail API quickstart example
├── credentials.json     # OAuth client credentials (from Google Cloud)
├── token.json           # User access/refresh tokens (auto-generated)
├── pyproject.toml       # Project dependencies and metadata
└── README.md
```

## Pydantic Models

### Job
Represents a single job listing:
- `title`: Job title
- `company`: Company name (optional)
- `location`: Job location (optional)
- `url`: LinkedIn job URL

### LinkedInJobAlert
Represents a parsed LinkedIn Job Alert email:
- `id`: Gmail message ID
- `subject`: Email subject
- `sender`: Sender email address
- `date`: Email date
- `snippet`: Email preview snippet
- `jobs`: List of `Job` objects

## Configuration

### Scopes

The application uses read-only access:

```python
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
```

To change scopes, modify the `SCOPES` variable and delete `token.json` to re-authenticate.

### Query Filters

Modify the query in `get_unread_messages_from_LinkedIn_JobAlerts()` to filter different messages:

| Query | Description |
|-------|-------------|
| `is:unread` | Unread messages |
| `is:unread in:inbox` | Unread in inbox only |
| `is:unread from:example@gmail.com` | Unread from specific sender |
| `is:unread after:2024/01/01` | Unread after a date |

## Dependencies

| Package | Purpose |
|---------|---------|
| `google-api-python-client` | Google API client library |
| `google-auth-httplib2` | HTTP transport for Google Auth |
| `google-auth-oauthlib` | OAuth2 authentication flow |
| `pydantic` | Data validation and JSON serialization |
| `beautifulsoup4` | HTML parsing (optional, for HTML emails) |

## Security Notes

- Never commit `credentials.json` or `token.json` to version control
- Add them to `.gitignore`
- The `token.json` contains sensitive refresh tokens that grant access to your Gmail

## Deploying to Kubernetes

For headless/background service deployment:

1. Generate `token.json` locally by running the app once
2. Create a Kubernetes Secret:
   ```bash
   kubectl create secret generic gmail-credentials \
     --from-file=token.json \
     --from-file=credentials.json
   ```
3. Mount the secret in your deployment

The app automatically refreshes tokens, so as long as it runs periodically, credentials stay valid.

## License

MIT
