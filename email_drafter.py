"""
Email Drafter Module
Creates personalized cold emails for job applications using AI
"""
from typing import Dict, List
import os
from openai import OpenAI


class EmailDrafter:
    """Drafts personalized cold emails for job applications"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the email drafter
        
        Args:
            api_key: OpenAI API key (if None, will look for OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')  # Configurable model
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: No OpenAI API key provided. Email drafting will use templates only.")
    
    def draft_cold_email(self, user_profile: Dict, job: Dict, tone: str = "professional") -> str:
        """
        Draft a personalized cold email for a job application
        
        Args:
            user_profile: User's profile information
            job: Job listing information
            tone: Email tone (professional, casual, enthusiastic)
            
        Returns:
            Drafted email text
        """
        if self.client and self.api_key:
            return self._draft_with_ai(user_profile, job, tone)
        else:
            return self._draft_with_template(user_profile, job)
    
    def _draft_with_ai(self, user_profile: Dict, job: Dict, tone: str) -> str:
        """Draft email using OpenAI API"""
        try:
            prompt = f"""
            Draft a compelling cold email for a job application with the following details:
            
            Candidate Information:
            - Name: {user_profile.get('name', 'Candidate')}
            - Skills: {', '.join(user_profile.get('skills', [])[:5])}
            - Experience: {user_profile.get('experience', 'Relevant experience in the field')}
            
            Job Information:
            - Title: {job.get('title', 'Position')}
            - Company: {job.get('company', 'Startup')}
            - Description: {job.get('description', 'Exciting opportunity at a growing startup')}
            
            Requirements:
            - Tone: {tone}
            - Length: 150-200 words
            - Include: Brief introduction, why they're a good fit, and call to action
            - Make it personalized and authentic
            - Show enthusiasm for startups and the specific company
            - Highlight relevant skills that match the job
            
            Format the email with proper structure (greeting, body, closing).
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert career coach who writes compelling job application emails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error drafting with AI: {e}")
            return self._draft_with_template(user_profile, job)
    
    def _draft_with_template(self, user_profile: Dict, job: Dict) -> str:
        """Draft email using a template (fallback when AI is not available)"""
        name = user_profile.get('name', 'Candidate')
        skills = user_profile.get('skills', [])
        top_skills = ', '.join(skills[:3]) if skills else 'relevant technical skills'
        
        job_title = job.get('title', 'Position')
        company = job.get('company', 'your company')
        
        email = f"""Subject: Application for {job_title} at {company}

Dear Hiring Manager,

I hope this email finds you well. My name is {name}, and I'm reaching out regarding the {job_title} position at {company}.

I'm particularly excited about this opportunity because of my strong background in {top_skills}. I've been following the startup ecosystem closely and am impressed by {company}'s innovative approach and growth trajectory.

My experience aligns well with this role, and I believe I can contribute significantly to your team from day one. I'm passionate about working in fast-paced startup environments where I can make a real impact.

I would love to discuss how my skills and experience could benefit {company}. Would you be available for a brief call this week?

Thank you for considering my application. I look forward to hearing from you.

Best regards,
{name}"""
        
        return email
    
    def draft_multiple_emails(self, user_profile: Dict, jobs: List[Dict], limit: int = 5) -> List[Dict]:
        """
        Draft emails for multiple job applications
        
        Args:
            user_profile: User's profile information
            jobs: List of job listings
            limit: Maximum number of emails to draft
            
        Returns:
            List of dictionaries with job info and drafted email
        """
        drafted_emails = []
        
        for job in jobs[:limit]:
            email_text = self.draft_cold_email(user_profile, job)
            drafted_emails.append({
                'job': job,
                'email': email_text,
                'subject': f"Application for {job.get('title', 'Position')} at {job.get('company', 'Company')}"
            })
        
        return drafted_emails
