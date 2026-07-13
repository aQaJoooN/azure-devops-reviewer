# Azure DevOps Build Reviewer

A Flask-based webhook application that receives Azure DevOps build completion notifications and aggregates build logs for AI-powered review.

## Features

-  Webhook endpoint for Azure DevOps build completion events
-  Automatic build log aggregation from Azure DevOps on-premise
-  Configurable retry mechanism for API calls
-  Error handling and validation
-  AI-powered build log analysis and review
-  Automated markdown review reports
-  Review submission back to Azure DevOps pipeline

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (see Configuration section)

3. Run the application:
```bash
python test.py
```

## Configuration

Configure the application using environment variables:

### Required Settings

- `AZR_AZURE_TOKEN` - Azure DevOps Personal Access Token (PAT) with build read permissions
- `AZR_AI_URL` - AI API endpoint URL
- `AZR_AI_KEY` - AI API authentication key

### Optional Settings

- `AZR_ENV` - Environment mode (default: "production")
- `AZR_DEBUG` - Enable debug mode (default: 0)
- `AZR_TESTING` - Enable testing mode (default: 0)
- `AZR_LOG_LEVEL` - Logging level: DEBUG, INFO, WARN, ERROR (default: "WARN")
- `AZR_TIMEOUT` - HTTP request timeout in seconds (default: 30)
- `AZR_RETRY` - Number of retry attempts for failed requests (default: 5)

### Example Configuration

Create a `.env` file in the project root:

```bash
AZR_ENV=development
AZR_DEBUG=1
AZR_LOG_LEVEL=DEBUG
AZR_AZURE_TOKEN=your_azure_devops_pat_token_here
AZR_TIMEOUT=60
AZR_RETRY=3
AZR_AI_URL=https://your-ai-endpoint.azurewebsites.net/api/review
AZR_AI_KEY=your_ai_api_key_here
```

## API Endpoints

### GET /webhook
Returns current application configuration (for debugging)

**Response:**
```json
{
  "AI_URL": "...",
  "LOG_LEVEL": "DEBUG",
  "RETRY": 3,
  "TIMEOUT": 60,
  "TESTING": 0,
  "DEBUG": 1,
  "ENV": "development"
}
```

### POST /webhook/pipeline
Webhook endpoint for Azure DevOps build completion events

**Request:** Azure DevOps webhook payload (application/json)

**Response:**
```json
{
  "status": "success",
  "build_id": "12345",
  "message": "Logs processed successfully"
}
```

## Azure DevOps Setup

1. Go to your Azure DevOps project settings
2. Navigate to Service Hooks
3. Create a new webhook subscription:
   - **Event**: Build completed
   - **URL**: `http://your-server-url/webhook/pipeline`
   - **Content Type**: application/json

## Logging

The application uses structured logging with the following levels:

- **DEBUG**: Detailed diagnostic information (API calls, response sizes, etc.)
- **INFO**: General informational messages (build processing, successful operations)
- **WARN**: Warning messages (invalid requests, failed downloads)
- **ERROR**: Error messages with stack traces (failed API calls, exceptions)

Set the `AZR_LOG_LEVEL` environment variable to control verbosity.

## Development

### Project Structure

```
azReviewer/
├── config/         # Configuration management
├── controller/     # Business logic
├── model/          # Data models (future)
├── util/           # Utility functions
│   ├── azureUtils.py   # Azure DevOps API client
│   └── logUtils.py     # Log aggregation
└── view/           # API endpoints
```

### Running in Development Mode

```bash
# Set environment variables
export AZR_ENV=development
export AZR_DEBUG=1
export AZR_LOG_LEVEL=DEBUG

# Run the app
python test.py
```

## Security Notes

- SSL verification is disabled for on-premise Azure DevOps (modify `azureUtils.py` if using trusted certificates)
- Azure DevOps PAT token should have minimal required permissions (Build: Read)
- Consider implementing webhook signature verification for production use

## License

See LICENSE file for details.
