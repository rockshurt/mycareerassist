# Configuration Template for MyCareerAssist

## Environment Variables
Create a `.streamlit/secrets.toml` file in your project root with the following:

```toml
# OpenAI API Configuration
OPENAI_API_KEY = "your-openai-api-key-here"
OPENAI_MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper

# Optional: LinkedIn API (if you plan to integrate)
LINKEDIN_API_KEY = "your-linkedin-api-key"
LINKEDIN_API_SECRET = "your-linkedin-api-secret"

# Database Configuration (if using a database)
DATABASE_URL = "sqlite:///mycareerassist.db"  # or PostgreSQL URL

# App Configuration
MAX_FILE_SIZE_MB = 10
SEARCH_RESULTS_PER_PAGE = 20
CACHE_EXPIRY_HOURS = 24

# Arbeitsagentur API (Usually no key needed, but keep for future use)
ARBEITSAGENTUR_API_URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/app/jobs"
```

## Streamlit Configuration
Create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#F8F9FA"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "minimal"

[browser]
gatherUsageStats = false

[logger]
level = "info"
```

## How to Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to https://share.streamlit.io/
3. Click "New app"
4. Select your repository
5. Set main file to "MyCareerAssist.py"
6. Add secrets in the deployment settings (Settings → Secrets)
7. Deploy!

## Local Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/MyCareerAssist.git
cd MyCareerAssist

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .streamlit directory and secrets
mkdir .streamlit
# Create secrets.toml with your API keys

# Run the app
streamlit run MyCareerAssist.py
```

## Testing

```bash
# Run tests (if you add a tests directory)
pytest tests/

# Check code quality
pylint MyCareerAssist.py

# Format code
black MyCareerAssist.py
```
