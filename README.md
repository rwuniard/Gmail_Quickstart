# Gmail Quickstart

A Python application that uses the Gmail API to read emails, with a focus on fetching unread LinkedIn Job Alert messages.

## Features

- OAuth2 authentication with Google
- List Gmail labels
- Fetch unread messages with full body content
- Filter for LinkedIn Job Alerts specifically
- Handles multipart email formats (plain text and HTML)

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

   Or with pip:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
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

Run the application:

```bash
uv run quickstart.py
```

Or with Python directly:

```bash
python quickstart.py
```

On first run, a browser window will open for Google authentication. After granting permissions, a `token.json` file will be created to store your credentials for future runs.

## How It Works

1. **Authentication**: The app checks for existing credentials in `token.json`. If not found or expired, it initiates the OAuth flow.

2. **List Labels**: Displays all Gmail labels in your account.

3. **Fetch Unread Messages**: Retrieves unread messages, filtering specifically for emails from LinkedIn Job Alerts.

4. **Extract Content**: Parses email body from both simple and multipart messages, handling base64 decoding.

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

## Files

| File | Description |
|------|-------------|
| `quickstart.py` | Main application code |
| `credentials.json` | OAuth client credentials (from Google Cloud) |
| `token.json` | User access/refresh tokens (auto-generated) |
| `pyproject.toml` | Project dependencies and metadata |

## Security Notes

- Never commit `credentials.json` or `token.json` to version control
- Add them to `.gitignore`
- The `token.json` contains sensitive refresh tokens that grant access to your Gmail

## License

MIT
