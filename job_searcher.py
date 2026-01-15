"""
Job Search Module
Searches for startup jobs matching user's profile and location
"""
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re


class JobSearcher:
    """Searches for startup jobs based on user profile and preferences"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_angellist_jobs(self, skills: List[str], location: str, limit: int = 10) -> List[Dict]:
        """
        Search for jobs on AngelList/Wellfound
        
        Args:
            skills: List of user's skills
            location: Job location
            limit: Maximum number of jobs to return
            
        Returns:
            List of job listings
        """
        jobs = []
        
        # Note: This is a simplified version. In production, you would use official APIs
        # or more sophisticated scraping with proper authentication
        
        search_terms = ' '.join(skills[:3]) if skills else 'software engineer'
        
        # Simulate job search results (in production, integrate with actual APIs)
        jobs.append({
            'title': f'{skills[0]} Engineer' if skills else 'Software Engineer',
            'company': 'Example Startup Inc.',
            'location': location,
            'description': f'Looking for a talented engineer with skills in {", ".join(skills[:3])}',
            'url': 'https://example.com/job1',
            'source': 'AngelList'
        })
        
        return jobs[:limit]
    
    def search_ycombinator_jobs(self, skills: List[str], location: str, limit: int = 10) -> List[Dict]:
        """
        Search for jobs from Y Combinator startups
        
        Args:
            skills: List of user's skills
            location: Job location
            limit: Maximum number of jobs to return
            
        Returns:
            List of job listings
        """
        jobs = []
        
        try:
            # Y Combinator Work at a Startup page
            url = "https://www.workatastartup.com/jobs"
            
            # Note: This is simplified. Real implementation would need proper API access
            jobs.append({
                'title': f'Engineer - {skills[0]}' if skills else 'Engineer',
                'company': 'YC Startup',
                'location': location,
                'description': f'Join our fast-growing startup. Required skills: {", ".join(skills[:3])}',
                'url': 'https://www.workatastartup.com/jobs/example',
                'source': 'Y Combinator'
            })
            
        except Exception as e:
            print(f"Error searching YC jobs: {e}")
        
        return jobs[:limit]
    
    def search_general_startup_jobs(self, skills: List[str], location: str, limit: int = 10) -> List[Dict]:
        """
        Search for startup jobs from various sources
        
        Args:
            skills: List of user's skills
            location: Job location
            limit: Maximum number of jobs to return
            
        Returns:
            List of job listings
        """
        jobs = []
        
        # Search terms based on skills
        search_query = f"startup {skills[0] if skills else 'engineer'} {location}"
        
        # Add sample jobs (in production, integrate with LinkedIn Jobs API, Indeed API, etc.)
        sample_jobs = [
            {
                'title': f'Senior {skills[0]} Developer' if skills else 'Senior Developer',
                'company': 'TechStartup Co.',
                'location': location,
                'description': f'Exciting opportunity at a growing startup. Skills needed: {", ".join(skills[:5])}',
                'url': 'https://example.com/job2',
                'source': 'LinkedIn'
            },
            {
                'title': f'{skills[0]} Engineer' if skills else 'Full Stack Engineer',
                'company': 'InnovateNow',
                'location': location,
                'description': 'Join our mission to revolutionize the industry. Early-stage startup with great growth potential.',
                'url': 'https://example.com/job3',
                'source': 'Indeed'
            }
        ]
        
        jobs.extend(sample_jobs)
        
        return jobs[:limit]
    
    def find_matching_jobs(self, user_profile: Dict, location: str, max_jobs: int = 20) -> List[Dict]:
        """
        Find jobs matching user's profile
        
        Args:
            user_profile: User's profile with skills and experience
            location: Desired job location
            max_jobs: Maximum number of jobs to return
            
        Returns:
            List of matching job listings
        """
        all_jobs = []
        skills = user_profile.get('skills', [])
        
        # Search multiple sources
        all_jobs.extend(self.search_angellist_jobs(skills, location, limit=7))
        all_jobs.extend(self.search_ycombinator_jobs(skills, location, limit=7))
        all_jobs.extend(self.search_general_startup_jobs(skills, location, limit=6))
        
        # Score and rank jobs based on skill match
        scored_jobs = self._score_jobs(all_jobs, skills)
        
        return scored_jobs[:max_jobs]
    
    def _score_jobs(self, jobs: List[Dict], user_skills: List[str]) -> List[Dict]:
        """
        Score and rank jobs based on skill match
        
        Args:
            jobs: List of job listings
            user_skills: User's skills
            
        Returns:
            Sorted list of jobs with match scores
        """
        for job in jobs:
            score = 0
            job_text = f"{job['title']} {job['description']}".lower()
            
            for skill in user_skills:
                if skill.lower() in job_text:
                    score += 1
            
            job['match_score'] = score
        
        # Sort by match score (descending)
        return sorted(jobs, key=lambda x: x.get('match_score', 0), reverse=True)
