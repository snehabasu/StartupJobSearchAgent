# Startup Job Search Agent 🚀

An intelligent AI agent that automates the job search process for startup positions. The agent parses your resume, finds your online presence (LinkedIn, GitHub, etc.), searches for matching startup jobs in your area, drafts personalized cold emails, and creates drafts in your Gmail account.

## Features

- 📄 **Resume Parsing**: Extracts key information from PDF resumes (name, email, skills, experience)
- 🔍 **Online Presence Discovery**: Automatically finds your LinkedIn profile, GitHub, and other online profiles
- 💼 **Startup Job Search**: Searches multiple sources (AngelList, Y Combinator, LinkedIn, Indeed) for matching startup jobs
- ✉️ **AI-Powered Email Drafting**: Creates personalized cold emails using OpenAI GPT for each job opportunity
- 📧 **Gmail Integration**: Automatically creates email drafts in your Gmail account for easy sending

## Prerequisites

- Python 3.7 or higher
- OpenAI API key (for AI-powered email drafting)
- Gmail API credentials (for Gmail integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/snehabasu/StartupJobSearchAgent.git
cd StartupJobSearchAgent
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Configure Gmail API (optional, for Gmail draft creation):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the project root
   - See [Google's Gmail API Quickstart](https://developers.google.com/gmail/api/quickstart/python) for detailed instructions

## Configuration

Edit the `.env` file with your settings:

```env
# OpenAI API key for AI-powered email drafting
OPENAI_API_KEY=your_openai_api_key_here

# Default job search location
DEFAULT_LOCATION=San Francisco, CA
SEARCH_RADIUS_MILES=50

# LinkedIn credentials (optional - for enhanced profile search)
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

## Usage

### Basic Usage

Run the agent with your resume:

```bash
python agent.py path/to/your/resume.pdf
```

You'll be prompted to enter your desired job location.

### Command Line Arguments

```bash
python agent.py <resume_path> [location]
```

Example:
```bash
python agent.py resume.pdf "New York, NY"
```

### What the Agent Does

1. **Parses Your Resume**: Extracts your name, email, phone, skills, and experience from your PDF resume
2. **Finds Your Online Presence**: Searches for your LinkedIn profile, GitHub, Twitter, and other online profiles
3. **Searches for Jobs**: Queries multiple startup job boards and platforms for positions matching your skills and location
4. **Ranks Jobs**: Scores jobs based on how well they match your skills
5. **Drafts Emails**: Creates personalized cold emails for each opportunity using AI
6. **Saves Drafts**: Saves all drafted emails to `email_drafts.txt` (and optionally creates Gmail drafts)

## Output

The agent generates:

- **email_drafts.txt**: Contains all drafted emails with job details
- **Console output**: Shows progress and summary of findings

Example output:
```
🚀 Startup Job Search Agent
================================================================================

📄 Step 1: Parsing your resume...
✓ Extracted profile for: John Doe
  Email: john.doe@example.com
  LinkedIn: https://linkedin.com/in/johndoe
  Skills: Python, JavaScript, React, AWS, Docker

🔍 Step 2: Finding your online presence...
✓ Found LinkedIn profile: https://linkedin.com/in/johndoe
✓ Found GitHub: https://github.com/johndoe

💼 Step 3: Searching for matching startup jobs...
  Location: San Francisco, CA
✓ Found 10 matching jobs:
  1. Python Engineer at Example Startup Inc.
     Match score: 5 | Source: AngelList
  ...

✉️  Step 4: Drafting personalized cold emails...
✓ Drafted 5 personalized emails

📧 Step 5: Creating Gmail drafts...
✓ Drafts saved to: email_drafts.txt
```

## Project Structure

```
StartupJobSearchAgent/
├── agent.py                 # Main application entry point
├── resume_parser.py         # Resume parsing module
├── linkedin_finder.py       # LinkedIn and online presence finder
├── job_searcher.py         # Job search module
├── email_drafter.py        # AI-powered email drafting
├── gmail_integration.py    # Gmail API integration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Features in Detail

### Resume Parser
- Extracts text from PDF resumes
- Identifies contact information (email, phone, LinkedIn)
- Detects skills from a comprehensive list of technologies
- Extracts work experience sections

### LinkedIn Finder
- Searches for LinkedIn profiles using Google
- Attempts to find GitHub, Twitter, and personal websites
- Can extract public profile information

### Job Searcher
- Searches multiple startup job platforms
- Ranks jobs based on skill match
- Returns comprehensive job details including company, location, and description

### Email Drafter
- Uses OpenAI GPT-3.5 to generate personalized emails
- Falls back to smart templates if API key is not provided
- Creates compelling, professional cold emails
- Customizes each email based on job and candidate profile

### Gmail Integration
- Authenticates with Gmail API using OAuth 2.0
- Creates email drafts that appear in your Gmail drafts folder
- Allows you to review and edit before sending

## Important Notes

- **Job Search**: The current implementation provides example job listings. For production use, integrate with official APIs from job boards (AngelList API, LinkedIn Jobs API, etc.)
- **LinkedIn Scraping**: LinkedIn has restrictions on automated scraping. Consider using their official API with proper authentication for production use.
- **Email Recipients**: The agent saves drafts locally. You'll need to find actual hiring manager email addresses before sending.
- **Privacy**: Never commit your `.env` file or `credentials.json` to version control.

## Troubleshooting

### "No OpenAI API key provided"
- Make sure you've added your OpenAI API key to the `.env` file
- The agent will fall back to template-based emails if no API key is provided

### "Gmail credentials file not found"
- Download your OAuth 2.0 credentials from Google Cloud Console
- Save the file as `credentials.json` in the project root
- See the Configuration section for detailed instructions

### "Could not extract information from resume"
- Ensure your resume is in PDF format
- Check that the PDF is not password-protected or image-based
- Try a different resume with clearer text formatting

## Future Enhancements

- [ ] Integration with official job board APIs
- [ ] Support for DOCX resume format
- [ ] Web interface for easier interaction
- [ ] Job application tracking database
- [ ] Automated follow-up email scheduling
- [ ] Support for cover letter generation
- [ ] Integration with more job platforms (Remote.co, Startup.jobs, etc.)
- [ ] Advanced LinkedIn profile analysis using official API
- [ ] Salary comparison and negotiation tips

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms included in the LICENSE file.

## Disclaimer

This tool is for educational and personal use. Always follow the terms of service of any platforms you interact with. Be respectful when sending cold emails and follow best practices for professional communication.
