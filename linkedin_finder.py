"""
LinkedIn Profile Finder Module
Searches for user's LinkedIn profile and extracts additional information
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re


class LinkedInFinder:
    """Finds and extracts information from LinkedIn profiles"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_profile(self, name: str, additional_info: str = "") -> Optional[str]:
        """
        Search for LinkedIn profile using Google search
        
        Args:
            name: Person's name
            additional_info: Additional information like company or location
            
        Returns:
            LinkedIn profile URL if found
        """
        query = f"{name} {additional_info} site:linkedin.com/in/"
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for LinkedIn URLs in search results
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if 'linkedin.com/in/' in href:
                    # Extract the actual LinkedIn URL
                    match = re.search(r'(https://[a-z]{2,3}\.linkedin\.com/in/[^&]+)', href)
                    if match:
                        return match.group(1)
        except Exception as e:
            print(f"Error searching for LinkedIn profile: {e}")
        
        return None
    
    def get_profile_info(self, linkedin_url: str) -> Dict:
        """
        Extract public information from LinkedIn profile
        
        Note: This is limited due to LinkedIn's restrictions on scraping.
        For production, use LinkedIn API with proper authentication.
        
        Args:
            linkedin_url: LinkedIn profile URL
            
        Returns:
            Dictionary with extracted profile information
        """
        profile_info = {
            'url': linkedin_url,
            'headline': None,
            'location': None,
            'current_company': None
        }
        
        try:
            response = requests.get(linkedin_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic info from public profile
            # Note: LinkedIn's structure changes frequently and scraping is limited
            
            # Try to find headline
            headline_element = soup.find('h2', class_=re.compile('headline|subtitle'))
            if headline_element:
                profile_info['headline'] = headline_element.text.strip()
            
            # Try to find location
            location_element = soup.find('span', class_=re.compile('location|region'))
            if location_element:
                profile_info['location'] = location_element.text.strip()
                
        except Exception as e:
            print(f"Error extracting profile info: {e}")
        
        return profile_info
    
    def find_additional_online_presence(self, name: str, email: str) -> Dict[str, str]:
        """
        Search for additional online presence (GitHub, Twitter, personal website)
        
        Args:
            name: Person's name
            email: Email address
            
        Returns:
            Dictionary with found online profiles
        """
        online_presence = {
            'github': None,
            'twitter': None,
            'personal_website': None
        }
        
        # Extract username from email
        username = email.split('@')[0] if email else ''
        
        # Search for GitHub
        github_possibilities = [
            f"https://github.com/{username}",
            f"https://github.com/{name.lower().replace(' ', '-')}",
            f"https://github.com/{name.lower().replace(' ', '')}"
        ]
        
        for github_url in github_possibilities:
            try:
                response = requests.head(github_url, timeout=5)
                if response.status_code == 200:
                    online_presence['github'] = github_url
                    break
            except requests.RequestException:
                continue
        
        # Search for Twitter
        twitter_possibilities = [
            f"https://twitter.com/{username}",
            f"https://twitter.com/{name.lower().replace(' ', '')}"
        ]
        
        for twitter_url in twitter_possibilities:
            try:
                response = requests.head(twitter_url, timeout=5)
                if response.status_code == 200:
                    online_presence['twitter'] = twitter_url
                    break
            except requests.RequestException:
                continue
        
        return online_presence
