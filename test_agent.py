"""
Example test file for the Startup Job Search Agent
Note: This is a basic test structure. Expand as needed.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import ResumeParser
from linkedin_finder import LinkedInFinder
from job_searcher import JobSearcher
from email_drafter import EmailDrafter


class TestResumeParser(unittest.TestCase):
    """Test cases for ResumeParser"""
    
    def setUp(self):
        self.parser = ResumeParser()
    
    def test_email_pattern(self):
        """Test email extraction pattern"""
        import re
        text = "Contact me at john.doe@example.com or jane@test.org"
        matches = re.findall(self.parser.email_pattern, text)
        self.assertIn('john.doe@example.com', matches)
        self.assertIn('jane@test.org', matches)
    
    def test_extract_skills(self):
        """Test skill extraction"""
        text = "I have experience with Python, JavaScript, React, and AWS"
        skills = self.parser._extract_skills(text)
        self.assertIn('Python', skills)
        self.assertIn('JavaScript', skills)
        self.assertIn('React', skills)
        self.assertIn('AWS', skills)


class TestJobSearcher(unittest.TestCase):
    """Test cases for JobSearcher"""
    
    def setUp(self):
        self.searcher = JobSearcher()
    
    def test_score_jobs(self):
        """Test job scoring based on skills"""
        jobs = [
            {
                'title': 'Python Developer',
                'description': 'Looking for Python and Django expert'
            },
            {
                'title': 'Java Developer',
                'description': 'Java and Spring Boot required'
            }
        ]
        
        user_skills = ['Python', 'Django', 'JavaScript']
        scored_jobs = self.searcher._score_jobs(jobs, user_skills)
        
        # Python job should score higher
        self.assertGreater(scored_jobs[0]['match_score'], scored_jobs[1]['match_score'])
        self.assertEqual(scored_jobs[0]['title'], 'Python Developer')


class TestEmailDrafter(unittest.TestCase):
    """Test cases for EmailDrafter"""
    
    def setUp(self):
        self.drafter = EmailDrafter(api_key=None)  # Use template mode
    
    def test_draft_with_template(self):
        """Test email drafting with template"""
        user_profile = {
            'name': 'John Doe',
            'skills': ['Python', 'JavaScript', 'React'],
            'email': 'john@example.com'
        }
        
        job = {
            'title': 'Full Stack Engineer',
            'company': 'TestStartup Inc.',
            'description': 'Looking for a talented engineer'
        }
        
        email = self.drafter._draft_with_template(user_profile, job)
        
        self.assertIn('John Doe', email)
        self.assertIn('Full Stack Engineer', email)
        self.assertIn('TestStartup Inc.', email)
        self.assertIn('Python', email)


class TestLinkedInFinder(unittest.TestCase):
    """Test cases for LinkedInFinder"""
    
    def setUp(self):
        self.finder = LinkedInFinder()
    
    def test_initialization(self):
        """Test LinkedInFinder initialization"""
        self.assertIsNotNone(self.finder.headers)
        self.assertIn('User-Agent', self.finder.headers)


if __name__ == '__main__':
    unittest.main()
