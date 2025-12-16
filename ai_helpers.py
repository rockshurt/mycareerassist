"""
AI Helper functions for MyCareerAssist
This module provides utilities for AI-powered features like resume optimization,
cover letter generation, and job matching.
"""

from typing import List, Dict, Tuple
import re


class ResumOptimizer:
    """Handles resume optimization for ATS systems and AI recommendations"""
    
    ATS_KEYWORDS = {
        'technical': [
            'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'AWS', 'Azure',
            'Machine Learning', 'Data Analysis', 'REST API', 'Docker', 'Kubernetes'
        ],
        'soft_skills': [
            'Leadership', 'Communication', 'Problem-Solving', 'Team Collaboration',
            'Project Management', 'Agile', 'Scrum', 'Critical Thinking'
        ],
        'achievements': [
            'Increased', 'Improved', 'Optimized', 'Implemented', 'Developed',
            'Designed', 'Led', 'Managed', 'Coordinated', 'Achieved'
        ]
    }
    
    ACTION_VERBS = [
        'Achieved', 'Analyzed', 'Built', 'Coordinated', 'Created', 'Designed',
        'Developed', 'Directed', 'Established', 'Executed', 'Implemented',
        'Improved', 'Led', 'Managed', 'Optimized', 'Organized', 'Pioneered',
        'Planned', 'Produced', 'Recognized', 'Reduced', 'Resolved', 'Spearheaded',
        'Streamlined', 'Supervised', 'Transformed', 'Coordinated'
    ]
    
    @staticmethod
    def get_missing_keywords(resume_text: str, job_description: str) -> List[str]:
        """
        Identifies missing keywords from job description in resume.
        
        Args:
            resume_text: The resume text
            job_description: The job posting text
        
        Returns:
            List of missing important keywords
        """
        missing = []
        
        # Extract keywords from job description
        keywords = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', job_description)
        
        for keyword in set(keywords):
            if keyword.lower() not in resume_text.lower():
                missing.append(keyword)
        
        return missing[:10]  # Return top 10
    
    @staticmethod
    def get_weak_verbs(resume_text: str) -> List[Tuple[str, str]]:
        """
        Identifies weak action verbs that should be replaced.
        
        Args:
            resume_text: The resume text
        
        Returns:
            List of (weak_verb, suggested_verb) tuples
        """
        weak_verbs = {
            'worked': 'Implemented',
            'did': 'Accomplished',
            'made': 'Created',
            'was responsible for': 'Managed',
            'helped': 'Supported',
            'responsible': 'Directed',
            'participated': 'Contributed',
            'involved': 'Executed',
        }
        
        suggestions = []
        for weak, strong in weak_verbs.items():
            if re.search(r'\b' + weak + r'\b', resume_text, re.IGNORECASE):
                suggestions.append((weak, strong))
        
        return suggestions
    
    @staticmethod
    def generate_ats_recommendations(resume_text: str) -> Dict[str, List[str]]:
        """
        Generates comprehensive ATS optimization recommendations.
        
        Args:
            resume_text: The resume text
        
        Returns:
            Dictionary with recommendation categories
        """
        recommendations = {
            'formatting': [],
            'keywords': [],
            'structure': [],
            'content': []
        }
        
        # Formatting checks
        if len(resume_text.split('\n')) < 10:
            recommendations['formatting'].append(
                "Resume appears too short. Add more details about your experience."
            )
        
        if not re.search(r'\b\d{4}\b', resume_text):
            recommendations['formatting'].append(
                "Consider adding dates to your work experience entries."
            )
        
        # Keyword checks
        if not re.search(r'(Python|Java|C\+\+|JavaScript|SQL)', resume_text):
            recommendations['keywords'].append(
                "Add relevant technical skills/programming languages if applicable."
            )
        
        if not re.search(r'(Project|Team|Leadership|Management)', resume_text):
            recommendations['keywords'].append(
                "Highlight leadership and management experience when relevant."
            )
        
        # Structure checks
        sections = ['Experience', 'Education', 'Skills', 'Summary']
        for section in sections:
            if not re.search(rf'\b{section}\b', resume_text, re.IGNORECASE):
                recommendations['structure'].append(
                    f"Consider adding a '{section}' section to your resume."
                )
        
        # Content checks
        weak_verbs = ResumOptimizer.get_weak_verbs(resume_text)
        if weak_verbs:
            recommendations['content'].append(
                f"Replace weak verbs like '{weak_verbs[0][0]}' with stronger action verbs."
            )
        
        return recommendations


class CoverLetterGenerator:
    """Generates customized cover letters using resume and job description"""
    
    TEMPLATES = {
        'formal_de': """Sehr geehrte Damen und Herren,

ich bin eine hochmotivierte Fachkraft mit {years} Jahren Erfahrung in {field}.
Meine Fähigkeiten im Bereich {skills} sowie meine {achievements} qualifizieren mich
ideal für die Position als {position} bei Ihrer Organisation.

In meiner bisherigen Karriere habe ich {accomplishments}.
Ich bin überzeugt, dass meine Kompetenzen und meine Leidenschaft für {passion}
einen wertvollen Beitrag zu Ihrem Team leisten werden.

Gerne stelle ich Ihnen in einem persönlichen Gespräch meine Qualifikationen 
näher dar. Vielen Dank für Ihre Aufmerksamkeit.

Mit freundlichen Grüßen,
{name}""",
        
        'formal_en': """Dear Hiring Manager,

I am a highly motivated professional with {years} years of experience in {field}.
My expertise in {skills} and proven track record of {achievements} make me
an excellent fit for the {position} role at your organization.

Throughout my career, I have {accomplishments}.
I am confident that my skills and passion for {passion} will make a
significant contribution to your team.

I would welcome the opportunity to discuss how I can add value to your organization.
Thank you for considering my application.

Best regards,
{name}"""
    }
    
    @staticmethod
    def generate_cover_letter(
        template: str,
        name: str,
        position: str,
        experience: Dict[str, str]
    ) -> str:
        """
        Generates a customized cover letter.
        
        Args:
            template: Template name ('formal_de', 'formal_en', etc.)
            name: Jobseeker's name
            position: Target position
            experience: Dictionary with experience details
        
        Returns:
            Generated cover letter
        """
        if template not in CoverLetterGenerator.TEMPLATES:
            template = 'formal_de'
        
        template_text = CoverLetterGenerator.TEMPLATES[template]
        
        # Fill placeholders
        cover_letter = template_text.format(
            name=name,
            position=position,
            years=experience.get('years', '5'),
            field=experience.get('field', 'your industry'),
            skills=experience.get('skills', 'relevant skills'),
            achievements=experience.get('achievements', 'consistent achievements'),
            accomplishments=experience.get('accomplishments', 'demonstrated excellence'),
            passion=experience.get('passion', 'professional growth')
        )
        
        return cover_letter


class JobMatcher:
    """Matches jobs with candidate profile"""
    
    @staticmethod
    def extract_candidate_profile(resume_text: str) -> Dict[str, any]:
        """
        Extracts candidate profile from resume.
        
        Args:
            resume_text: The resume text
        
        Returns:
            Dictionary with extracted profile data
        """
        profile = {
            'skills': [],
            'experience_years': 0,
            'languages': [],
            'education_level': 'Unknown',
            'key_achievements': []
        }
        
        # Extract skills (simple pattern matching)
        skill_patterns = r'\b(Python|Java|SQL|AWS|Azure|Docker|Kubernetes|React|Angular)\b'
        profile['skills'] = re.findall(skill_patterns, resume_text, re.IGNORECASE)
        
        # Extract years of experience
        years_pattern = r'(\d+)\s+(?:years?|Jahre|Jahres?)'
        years_matches = re.findall(years_pattern, resume_text, re.IGNORECASE)
        if years_matches:
            profile['experience_years'] = max(int(y) for y in years_matches)
        
        # Extract languages
        languages = ['English', 'German', 'French', 'Spanish', 'Chinese']
        profile['languages'] = [lang for lang in languages if lang in resume_text]
        
        # Extract education level
        if re.search(r'(Master|M\.Sc|MBA)', resume_text):
            profile['education_level'] = 'Master'
        elif re.search(r'(Bachelor|B\.Sc|B\.A)', resume_text):
            profile['education_level'] = 'Bachelor'
        elif re.search(r'(Diplom|Diplom|Certification)', resume_text):
            profile['education_level'] = 'Diploma/Certification'
        
        return profile
    
    @staticmethod
    def calculate_job_match_score(
        candidate_profile: Dict[str, any],
        job_description: str
    ) -> float:
        """
        Calculates match score between candidate and job (0-100).
        
        Args:
            candidate_profile: Extracted candidate profile
            job_description: Job posting text
        
        Returns:
            Match score (0-100)
        """
        score = 0
        max_score = 100
        
        # Skills matching
        candidate_skills = set(s.lower() for s in candidate_profile.get('skills', []))
        job_skills = set(re.findall(r'\b(Python|Java|SQL|AWS|Azure|Docker)\b', 
                                    job_description, re.IGNORECASE))
        
        if job_skills:
            skill_match = len(candidate_skills & job_skills) / len(job_skills) * 40
            score += skill_match
        else:
            score += 40
        
        # Experience matching
        experience_req = re.search(r'(\d+)\s+(?:years?|Jahre)', job_description)
        if experience_req:
            req_years = int(experience_req.group(1))
            if candidate_profile['experience_years'] >= req_years:
                score += 30
            else:
                score += max(0, (candidate_profile['experience_years'] / req_years) * 30)
        else:
            score += 30
        
        # Education matching
        if 'Master' in job_description and candidate_profile['education_level'] == 'Master':
            score += 20
        elif 'Bachelor' in job_description and candidate_profile['education_level'] in ['Master', 'Bachelor']:
            score += 15
        elif candidate_profile['education_level'] != 'Unknown':
            score += 10
        
        return min(100, score)
