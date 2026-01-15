#!/usr/bin/env python3
"""
Startup Job Search Agent
Main application that orchestrates all modules to help users find startup jobs
"""
import os
import sys
from dotenv import load_dotenv
from resume_parser import ResumeParser
from linkedin_finder import LinkedInFinder
from job_searcher import JobSearcher
from email_drafter import EmailDrafter
from gmail_integration import GmailIntegration
from typing import Dict, List


class StartupJobSearchAgent:
    """Main agent that coordinates the job search process"""
    
    def __init__(self):
        load_dotenv()
        self.resume_parser = ResumeParser()
        self.linkedin_finder = LinkedInFinder()
        self.job_searcher = JobSearcher()
        self.email_drafter = EmailDrafter()
        self.gmail_integration = None
    
    def run(self, resume_path: str, location: str = None):
        """
        Run the complete job search agent workflow
        
        Args:
            resume_path: Path to the resume PDF file
            location: Job search location (optional, uses default from .env)
        """
        print("=" * 80)
        print("🚀 Startup Job Search Agent")
        print("=" * 80)
        print()
        
        # Step 1: Parse resume
        print("📄 Step 1: Parsing your resume...")
        user_profile = self.resume_parser.parse_resume(resume_path)
        
        if not user_profile.get('name'):
            print("Error: Could not extract information from resume. Please check the file.")
            return
        
        print(f"✓ Extracted profile for: {user_profile['name']}")
        print(f"  Email: {user_profile.get('email', 'Not found')}")
        print(f"  LinkedIn: {user_profile.get('linkedin_url', 'Not found')}")
        print(f"  Skills: {', '.join(user_profile.get('skills', [])[:5])}")
        print()
        
        # Step 2: Find LinkedIn and online presence
        print("🔍 Step 2: Finding your online presence...")
        
        if not user_profile.get('linkedin_url') and user_profile.get('name'):
            linkedin_url = self.linkedin_finder.search_profile(
                user_profile['name'],
                user_profile.get('email', '')
            )
            if linkedin_url:
                user_profile['linkedin_url'] = linkedin_url
                print(f"✓ Found LinkedIn profile: {linkedin_url}")
        
        if user_profile.get('email'):
            online_presence = self.linkedin_finder.find_additional_online_presence(
                user_profile['name'],
                user_profile['email']
            )
            user_profile['online_presence'] = online_presence
            
            if online_presence.get('github'):
                print(f"✓ Found GitHub: {online_presence['github']}")
            if online_presence.get('twitter'):
                print(f"✓ Found Twitter: {online_presence['twitter']}")
        print()
        
        # Step 3: Search for jobs
        print("💼 Step 3: Searching for matching startup jobs...")
        
        search_location = location or os.getenv('DEFAULT_LOCATION', 'San Francisco, CA')
        print(f"  Location: {search_location}")
        
        jobs = self.job_searcher.find_matching_jobs(user_profile, search_location, max_jobs=10)
        
        print(f"✓ Found {len(jobs)} matching jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"  {i}. {job['title']} at {job['company']}")
            print(f"     Match score: {job.get('match_score', 0)} | Source: {job.get('source', 'N/A')}")
        print()
        
        # Step 4: Draft cold emails
        print("✉️  Step 4: Drafting personalized cold emails...")
        
        drafted_emails = self.email_drafter.draft_multiple_emails(
            user_profile, 
            jobs, 
            limit=5
        )
        
        print(f"✓ Drafted {len(drafted_emails)} personalized emails")
        print()
        
        # Step 5: Create Gmail drafts
        print("📧 Step 5: Creating Gmail drafts...")
        
        try:
            self.gmail_integration = GmailIntegration()
            
            if self.gmail_integration.service:
                # Save drafts locally first
                self._save_drafts_locally(drafted_emails)
                
                print("  Note: Gmail API requires actual recipient email addresses.")
                print("  Drafts have been saved locally to 'email_drafts.txt'")
                print("  You can manually create Gmail drafts or update recipient emails and run again.")
                
                # Uncomment the following lines when you have actual recipient emails
                # draft_results = self.gmail_integration.create_multiple_drafts(drafted_emails)
                # print(f"✓ Created {len(draft_results)} drafts in Gmail")
                
        except Exception as e:
            print(f"  Could not connect to Gmail: {e}")
            print("  Saving drafts locally instead...")
            self._save_drafts_locally(drafted_emails)
        
        print()
        print("=" * 80)
        print("✅ Job search complete!")
        print("=" * 80)
        print()
        print("Summary:")
        print(f"  • Profile parsed: {user_profile['name']}")
        print(f"  • Jobs found: {len(jobs)}")
        print(f"  • Emails drafted: {len(drafted_emails)}")
        print(f"  • Drafts saved to: email_drafts.txt")
        print()
        print("Next steps:")
        print("  1. Review the drafted emails in 'email_drafts.txt'")
        print("  2. Customize them as needed")
        print("  3. Send them to the companies or create Gmail drafts manually")
        print()
    
    def _save_drafts_locally(self, drafted_emails: List[Dict]):
        """Save drafted emails to a local file"""
        with open('email_drafts.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("DRAFTED JOB APPLICATION EMAILS\n")
            f.write("=" * 80 + "\n\n")
            
            for i, email_data in enumerate(drafted_emails, 1):
                job = email_data['job']
                f.write(f"\n{'=' * 80}\n")
                f.write(f"EMAIL #{i}\n")
                f.write(f"{'=' * 80}\n\n")
                f.write(f"To: [Find hiring manager email for {job['company']}]\n")
                f.write(f"Subject: {email_data['subject']}\n\n")
                f.write(f"Job Details:\n")
                f.write(f"  Title: {job['title']}\n")
                f.write(f"  Company: {job['company']}\n")
                f.write(f"  Location: {job['location']}\n")
                f.write(f"  URL: {job.get('url', 'N/A')}\n")
                f.write(f"  Match Score: {job.get('match_score', 0)}\n\n")
                f.write(f"Email Body:\n")
                f.write(f"{'-' * 80}\n")
                f.write(f"{email_data['email']}\n")
                f.write(f"{'-' * 80}\n\n")
        
        print(f"✓ Drafts saved to: email_drafts.txt")


def main():
    """Main entry point"""
    print("Welcome to the Startup Job Search Agent!")
    print()
    
    # Get resume path
    if len(sys.argv) > 1:
        resume_path = sys.argv[1]
    else:
        resume_path = input("Please enter the path to your resume (PDF): ").strip()
    
    if not os.path.exists(resume_path):
        print(f"Error: Resume file not found at {resume_path}")
        return
    
    # Get location
    location = None
    if len(sys.argv) > 2:
        location = sys.argv[2]
    else:
        location_input = input("Enter job search location (press Enter for default): ").strip()
        if location_input:
            location = location_input
    
    # Run the agent
    agent = StartupJobSearchAgent()
    agent.run(resume_path, location)


if __name__ == "__main__":
    main()
