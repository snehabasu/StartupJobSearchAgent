"""
Gmail Integration Module
Connects to Gmail API to create email drafts
"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from typing import List, Dict


class GmailIntegration:
    """Integrates with Gmail API to create email drafts"""
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    
    def __init__(self, credentials_path: str = 'credentials.json'):
        """
        Initialize Gmail integration
        
        Args:
            credentials_path: Path to Gmail API credentials file
        """
        self.credentials_path = credentials_path
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"Error: Gmail credentials file not found at {self.credentials_path}")
                    print("Please download credentials.json from Google Cloud Console")
                    print("See README.md for instructions")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("Successfully authenticated with Gmail API")
        except Exception as e:
            print(f"Error building Gmail service: {e}")
    
    def create_draft(self, to: str, subject: str, body: str) -> Dict:
        """
        Create an email draft in Gmail
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            Dictionary with draft information
        """
        if not self.service:
            print("Gmail service not initialized. Cannot create draft.")
            return {'error': 'Service not initialized'}
        
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            # Encode the message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            create_message = {
                'message': {
                    'raw': encoded_message
                }
            }
            
            # Create the draft
            draft = self.service.users().drafts().create(
                userId='me',
                body=create_message
            ).execute()
            
            print(f"Draft created with ID: {draft['id']}")
            return {
                'id': draft['id'],
                'subject': subject,
                'to': to,
                'status': 'created'
            }
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {'error': str(error)}
        except Exception as e:
            print(f"Error creating draft: {e}")
            return {'error': str(e)}
    
    def create_multiple_drafts(self, drafted_emails: List[Dict]) -> List[Dict]:
        """
        Create multiple email drafts in Gmail
        
        Args:
            drafted_emails: List of drafted email dictionaries
            
        Returns:
            List of draft creation results
        """
        results = []
        
        for email_data in drafted_emails:
            job = email_data.get('job', {})
            email_text = email_data.get('email', '')
            subject = email_data.get('subject', 'Job Application')
            
            # For cold emails, you might want to find the hiring manager's email
            # For now, we'll use a placeholder
            recipient = job.get('recruiter_email', 'hiring@company.com')
            
            result = self.create_draft(
                to=recipient,
                subject=subject,
                body=email_text
            )
            
            result['job_title'] = job.get('title', 'Unknown')
            result['company'] = job.get('company', 'Unknown')
            results.append(result)
        
        return results
    
    def list_drafts(self, max_results: int = 10) -> List[Dict]:
        """
        List existing drafts in Gmail
        
        Args:
            max_results: Maximum number of drafts to return
            
        Returns:
            List of draft information
        """
        if not self.service:
            print("Gmail service not initialized.")
            return []
        
        try:
            results = self.service.users().drafts().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            drafts = results.get('drafts', [])
            
            if not drafts:
                print('No drafts found.')
                return []
            
            draft_list = []
            for draft in drafts:
                draft_data = self.service.users().drafts().get(
                    userId='me',
                    id=draft['id']
                ).execute()
                
                message = draft_data['message']
                subject = None
                for header in message['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                        break
                
                draft_list.append({
                    'id': draft['id'],
                    'subject': subject,
                    'snippet': message.get('snippet', '')
                })
            
            return draft_list
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
