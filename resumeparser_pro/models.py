"""
Data models for resume parsing results
"""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class ContactInfo(BaseModel):
    """Contact information schema"""
    full_name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio/website URL")
    other_profiles: List[str] = Field(default_factory=list, description="Other profiles URL's")

class Education(BaseModel):
    """Education schema"""
    degree: Optional[str] = Field(None, description="Degree name")
    field_of_study: Optional[str] = Field(None, description="Major/specialization")
    institution: Optional[str] = Field(None, description="University/college name")
    location: Optional[str] = Field(None, description="Institution location")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")
    gpa: Optional[str] = Field(None, description="GPA or percentage")
    honors: List[str] = Field(default_factory=list, description="Academic honors")
    relevant_coursework: List[str] = Field(default_factory=list, description="Relevant courses")

class Experience(BaseModel):
    """Work experience schema"""
    job_title: Optional[str] = Field(None, description="Job title/role")
    company: Optional[str] = Field(None, description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    employment_type: Optional[str] = Field(None, description="Employment type")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")
    duration_months: Optional[int] = Field(None, description="Duration in months")
    description: Optional[str] = Field(None, description="Job description")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    achievements: List[str] = Field(default_factory=list, description="Achievements")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")

class Project(BaseModel):
    """Project schema"""
    name: Optional[str] = Field(None, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    role: Optional[str] = Field(None, description="Your role in the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    duration_months: Optional[int] = Field(None, description="Duration in months")
    team_size: Optional[str] = Field(None, description="Team size")
    key_features: List[str] = Field(default_factory=list, description="Key features")
    outcomes: List[str] = Field(default_factory=list, description="Project outcomes")
    links: List[str] = Field(default_factory=list, description="Project URLs")

class Certification(BaseModel):
    """Certification schema"""
    name: str = Field(..., description="Certification name")
    issuing_organization: Optional[str] = Field(None, description="Issuing organization")
    issue_date: Optional[str] = Field(None, description="Issue date")
    expiry_date: Optional[str] = Field(None, description="Expiry date")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    verification_url: Optional[str] = Field(None, description="Verification URL")

class Skill(BaseModel):
    """Skill schema"""
    category: str = Field(..., description="Skill category")
    skills: List[str] = Field(..., description="Skills in this category")
    proficiency_level: Optional[str] = Field(None, description="Proficiency level")

class Language(BaseModel):
    """Language schema"""
    language: str = Field(..., description="Language name")
    proficiency: Optional[str] = Field(None, description="Proficiency level")

class Publication(BaseModel):
    """Publication schema"""
    title: str = Field(..., description="Publication title")
    authors: List[str] = Field(default_factory=list, description="Authors")
    venue: Optional[str] = Field(None, description="Conference/journal")
    date: Optional[str] = Field(None, description="Publication date")
    url: Optional[str] = Field(None, description="Publication URL")

class Award(BaseModel):
    """Award schema"""
    title: str = Field(..., description="Award title")
    issuer: Optional[str] = Field(None, description="Issuing organization")
    date: Optional[str] = Field(None, description="Award date")
    description: Optional[str] = Field(None, description="Award description")

class ResumeSchema(BaseModel):
    """Complete resume schema"""
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    professional_summary: Optional[str] = Field(None, description="Professional summary")
    skills: List[Skill] = Field(default_factory=list, description="Categorized skills")
    work_experience: List[Experience] = Field(default_factory=list, description="Work experience")
    education: List[Education] = Field(default_factory=list, description="Education")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications")
    languages: List[Language] = Field(default_factory=list, description="Languages")
    publications: List[Publication] = Field(default_factory=list, description="Publications")
    awards: List[Award] = Field(default_factory=list, description="Awards")
    volunteer_experience: List[str] = Field(default_factory=list, description="Volunteer work")
    interests: List[str] = Field(default_factory=list, description="Interests")
    total_experience_months: Optional[int] = Field(None, description="Total experience in months")
    industry: Optional[str] = Field(None, description="Primary industry")
    seniority_level: Optional[str] = Field(None, description="Seniority level")

class ParsedResumeResult(BaseModel):
    """Result wrapper for parsed resume"""
    file_path: str = Field(..., description="Path to processed file")
    success: bool = Field(..., description="Whether parsing was successful")
    resume_data: Optional[ResumeSchema] = Field(None, description="Parsed resume data")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    parsing_time_seconds: float = Field(..., description="Parsing time")
    timestamp: str = Field(..., description="Processing timestamp")
