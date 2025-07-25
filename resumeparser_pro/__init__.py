"""
ResumeParser Pro - Production-ready resume parsing library with parallel processing
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "AI-powered resume parser with parallel processing capabilities"

from .parser import ResumeParserPro
from .models import (
    ContactInfo,
    Education, 
    Experience,
    Project,
    Certification,
    Skill,
    Language,
    Publication,
    Award,
    ResumeSchema,
    ParsedResumeResult
)

__all__ = [
    "ResumeParserPro",
    "ContactInfo",
    "Education",
    "Experience", 
    "Project",
    "Certification",
    "Skill",
    "Language",
    "Publication",
    "Award",
    "ResumeSchema",
    "ParsedResumeResult"
]
