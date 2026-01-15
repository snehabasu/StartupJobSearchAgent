"""
Resume Parser Module
Extracts information from PDF resumes
"""
import PyPDF2
import re
from typing import Dict, List


class ResumeParser:
    """Parses resume files and extracts key information"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def parse_resume(self, pdf_path: str) -> Dict:
        """Parse resume and extract key information"""
        text = self.extract_text_from_pdf(pdf_path)
        
        # Extract email
        email_matches = re.findall(self.email_pattern, text)
        email = email_matches[0] if email_matches else None
        
        # Extract phone
        phone_matches = re.findall(self.phone_pattern, text)
        phone = phone_matches[0] if phone_matches else None
        
        # Extract LinkedIn URL
        linkedin_matches = re.findall(self.linkedin_pattern, text, re.IGNORECASE)
        linkedin_url = f"https://{linkedin_matches[0]}" if linkedin_matches else None
        
        # Extract name (usually first line or first few words)
        lines = text.split('\n')
        name = None
        for line in lines:
            if line.strip() and len(line.strip()) > 3:
                name = line.strip()
                break
        
        # Extract skills (look for common skill keywords)
        skills = self._extract_skills(text)
        
        # Extract experience (look for years of experience or job titles)
        experience = self._extract_experience(text)
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'linkedin_url': linkedin_url,
            'skills': skills,
            'experience': experience,
            'full_text': text
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        common_skills = [
            'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'SQL', 'AWS',
            'Docker', 'Kubernetes', 'Git', 'Machine Learning', 'AI', 'Django',
            'Flask', 'Angular', 'Vue.js', 'TypeScript', 'MongoDB', 'PostgreSQL',
            'Redis', 'Kafka', 'REST API', 'GraphQL', 'Microservices', 'Agile',
            'TensorFlow', 'PyTorch', 'Data Analysis', 'Excel', 'Tableau',
            'Leadership', 'Project Management', 'Communication', 'Problem Solving'
        ]
        
        found_skills = []
        text_upper = text.upper()
        for skill in common_skills:
            if skill.upper() in text_upper:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience(self, text: str) -> str:
        """Extract experience information from resume"""
        # Look for experience section
        experience_keywords = ['EXPERIENCE', 'WORK HISTORY', 'EMPLOYMENT', 'PROFESSIONAL EXPERIENCE']
        lines = text.split('\n')
        
        experience_section = []
        in_experience = False
        
        for i, line in enumerate(lines):
            line_upper = line.upper().strip()
            if any(keyword in line_upper for keyword in experience_keywords):
                in_experience = True
                continue
            
            if in_experience:
                # Stop at next major section
                if any(keyword in line_upper for keyword in ['EDUCATION', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS']):
                    break
                if line.strip():
                    experience_section.append(line.strip())
        
        return ' '.join(experience_section[:500]) if experience_section else "Experience details not clearly extracted"
