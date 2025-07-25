"""
Main resume parser class
"""

import logging
import threading
from typing import List, Dict, Any, Union
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from langchain.chat_models import init_chat_model

from .models import ResumeSchema, ParsedResumeResult
from .extractors import TextExtractor, TextExtractorError
from .utils import PostProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParserError(Exception):
    """Custom exception for resume parsing errors"""
    pass

class ResumeParserPro:
    """
    Production-ready resume parser with AI and parallel processing
    
    Example:
        >>> parser = ResumeParserPro(
        ...     provider="google_genai",
        ...     model_name="gemini-2.0-flash", 
        ...     api_key="your-api-key"
        ... )
        >>> result = parser.parse_resume("resume.pdf")
        >>> batch_results = parser.parse_batch(["resume1.pdf", "resume2.docx"])
    """
    
    def __init__(
        self, 
        provider: str,
        model_name: str, 
        api_key: str,
        max_workers: int = 5,
        temperature: float = 0.1
    ):
        """
        Initialize the resume parser
        
        Args:
            provider: Model provider (e.g., "google_genai", "openai", "anthropic")
            model_name: Model name (e.g., "gemini-2.0-flash", "gpt-4o-mini")
            api_key: API key for the model provider
            max_workers: Number of parallel workers for batch processing
            temperature: Model temperature for consistency (0.0-1.0)
        """
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.max_workers = max_workers
        self.temperature = temperature
        self._thread_local = threading.local()
        
        # Validate inputs
        if not all([provider, model_name, api_key]):
            raise ValueError("Provider, model_name, and api_key are required")
        
        self.full_model_name = f"{provider}:{model_name}"
        self._validate_setup()
        
        logger.info(f"ResumeParserPro initialized with {self.full_model_name}")
    
    def _validate_setup(self):
        """Validate the model setup"""
        try:
            # Test model initialization
            test_model = init_chat_model(
                self.full_model_name,
                api_key=self.api_key,
                temperature=self.temperature
            )
            logger.info("✅ Model validation successful")
        except Exception as e:
            raise ResumeParserError(f"Model validation failed: {e}")
    
    def _get_thread_local_model(self):
        """Get or create thread-local model instance"""
        if not hasattr(self._thread_local, 'model'):
            try:
                model = init_chat_model(
                    self.full_model_name,
                    api_key=self.api_key,
                    temperature=self.temperature
                )
                self._thread_local.model = model.with_structured_output(ResumeSchema)
            except Exception as e:
                raise ResumeParserError(f"Thread-local model initialization failed: {e}")
        
        return self._thread_local.model
    
    def _create_parsing_prompt(self, text: str) -> str:
        """Create optimized prompt for resume parsing"""
        return f"""You are an expert resume parser and HR professional with 15+ years of experience. Your task is to extract information from resumes with maximum accuracy and attention to detail.

CRITICAL INSTRUCTIONS:
1. Extract ALL information present in the resume - don't skip details
2. Categorize skills properly (Programming Languages, Frameworks, Tools, Databases, etc.)
3. For dates: Use exact format from resume or standardize to YYYY-MM or YYYY
4. For experience: Extract quantifiable achievements separately from responsibilities
5. Parse tables and structured data carefully
6. Identify the candidate's seniority level based on experience and roles
7. Calculate total experience based on all roles
8. **IMPORTANT: ALL DURATION/EXPERIENCE VALUES MUST BE IN INTEGER MONTHS**
   - For "1 year 6 months" return 18
   - For "2 years" return 24
   - For "6 months" return 6
   - For "3.5 years" return 42

EXTRACTION GUIDELINES:

**Contact Information:**
- Extract full name (handle different name formats)
- Validate and extract email addresses
- Parse phone numbers (handle international formats)
- Extract location (city, state, country)
- Find all social profiles (LinkedIn, GitHub, portfolio, etc.)

**Skills Categorization:**
- Programming Languages: Python, Java, JavaScript, etc.
- Frameworks/Libraries: React, Django, Spring Boot, etc.
- Databases: MySQL, MongoDB, PostgreSQL, etc.
- Cloud/DevOps: AWS, Docker, Kubernetes, etc.
- Tools: Git, JIRA, VS Code, etc.
- Soft Skills: Leadership, Communication, etc.

**Experience Parsing (DURATION IN MONTHS ONLY):**
- Extract exact job titles and normalize if needed
- Company names and locations
- Employment type (Full-time, Part-time, Contract, Internship)
- Start and end dates with duration calculation IN MONTHS
- Separate responsibilities from achievements
- Extract technologies used in each role
- duration_months: INTEGER value only (e.g., 18 for 1.5 years)

**Education Details:**
- Full degree names and specializations
- Institution names and locations
- Graduation dates and GPAs
- Academic honors and relevant coursework

**Projects (DURATION IN MONTHS):**
- Project names and descriptions
- Your role and team size
- Technologies and tools used
- Project outcomes and key features
- Links to demos or repositories
- duration_months: INTEGER value only

**Additional Sections:**
- Certifications with issuing organizations and dates
- Publications with authors and venues
- Awards and honors with dates
- Language proficiency levels
- Volunteer work and interests

**METADATA (CRITICAL):**
- total_experience_months: INTEGER sum of all work experience in months
- industry: Primary industry/domain
- seniority_level: Junior/Mid/Senior based on total experience

RESUME TEXT TO PARSE:

{text}

---

IMPORTANT: Return a complete, accurate extraction. All duration fields MUST be integers representing months. If any field is not present in the resume, leave it as null/empty but don't skip parsing other sections. Be thorough and precise.
"""



    def parse_resume(self, file_path: Union[str, Path]) -> ParsedResumeResult:
        """
        Parse a single resume file
        
        Args:
            file_path: Path to the resume file (PDF, DOCX, or TXT)
            
        Returns:
            ParsedResumeResult object with parsed data or error information
        """
        start_time = datetime.now()
        file_path = str(file_path)
        
        try:
            logger.info(f"Parsing resume: {file_path}")
            
            # Extract text
            text = TextExtractor.extract_text(file_path)
            
            if not text or len(text.strip()) < 50:
                raise ResumeParserError("Extracted text is too short or empty")
            
            # Create prompt
            prompt = self._create_parsing_prompt(text)
            
            # Parse with AI model
            model = self._get_thread_local_model()
            response = model.invoke(prompt)
            
            if not response:
                raise ResumeParserError("AI model returned empty response")
            
            # Post-process results
            result_dict = response.model_dump()
            result_dict = self._post_process_result(result_dict)
            
            # Create successful result
            parsing_time = (datetime.now() - start_time).total_seconds()
            
            return ParsedResumeResult(
                file_path=file_path,
                success=True,
                resume_data=ResumeSchema(**result_dict),
                error_message=None,
                parsing_time_seconds=parsing_time,
                timestamp=datetime.now().isoformat()
            )
        
        except Exception as e:
            error_msg = str(e)
            parsing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Parsing failed for {file_path}: {error_msg}")
            
            return ParsedResumeResult(
                file_path=file_path,
                success=False,
                resume_data=None,
                error_message=error_msg,
                parsing_time_seconds=parsing_time,
                timestamp=datetime.now().isoformat()
            )
    
    def parse_batch(
        self, 
        file_paths: List[Union[str, Path]], 
        include_failed: bool = False
    ) -> List[ParsedResumeResult]:
        """
        Parse multiple resume files in parallel
        
        Args:
            file_paths: List of file paths to process
            include_failed: Whether to include failed results in output
            
        Returns:
            List of ParsedResumeResult objects
        """
        file_paths = [str(path) for path in file_paths]
        logger.info(f"Starting batch processing of {len(file_paths)} files with {self.max_workers} workers")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all parsing tasks
            future_to_path = {
                executor.submit(self.parse_resume, file_path): file_path 
                for file_path in file_paths
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_path):
                file_path = future_to_path[future]
                try:
                    result = future.result()
                    
                    if result.success or include_failed:
                        results.append(result)
                    
                    if result.success:
                        logger.info(f"✅ {file_path} ({result.parsing_time_seconds:.2f}s)")
                    else:
                        logger.error(f"❌ {file_path} - {result.error_message}")
                        
                except Exception as e:
                    logger.error(f"Unexpected error processing {file_path}: {e}")
                    if include_failed:
                        results.append(ParsedResumeResult(
                            file_path=file_path,
                            success=False,
                            resume_data=None,
                            error_message=f"Unexpected error: {e}",
                            parsing_time_seconds=0.0,
                            timestamp=datetime.now().isoformat()
                        ))
        
        # Sort results by file path
        results.sort(key=lambda x: x.file_path)
        
        successful_count = sum(1 for r in results if r.success)
        total_time = sum(r.parsing_time_seconds for r in results)
        
        logger.info(f"Batch completed: {successful_count}/{len(file_paths)} successful, "
                   f"total time: {total_time:.2f}s")
        
        return results
    
    def get_successful_resumes(self, results: List[ParsedResumeResult]) -> List[Dict[str, Any]]:
        """Extract only successful resume data from batch results"""
        successful_resumes = []
        
        for result in results:
            if result.success and result.resume_data:
                resume_dict = result.resume_data.model_dump()
                resume_dict['_metadata'] = {
                    'file_path': result.file_path,
                    'parsing_time_seconds': result.parsing_time_seconds,
                    'timestamp': result.timestamp,
                    'library_version': '1.0.0'
                }
                successful_resumes.append(resume_dict)
        
        return successful_resumes
    
    def get_summary(self, results: List[ParsedResumeResult]) -> Dict[str, Any]:
        """Get processing summary statistics"""
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]
        
        return {
            'total_files': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(results) * 100 if results else 0,
            'total_processing_time': sum(r.parsing_time_seconds for r in results),
            'avg_processing_time': sum(r.parsing_time_seconds for r in results) / len(results) if results else 0,
            'failed_files': [{'file_path': r.file_path, 'error': r.error_message} for r in failed]
        }
    
    def _post_process_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process and clean parsed results"""
        # Clean contact info
        if result.get('contact_info'):
            result['contact_info'] = PostProcessor.clean_contact_info(result['contact_info'])
        
        # Calculate experience durations if missing
        if result.get('work_experience'):
            for exp in result['work_experience']:
                if not exp.get('duration_months'):
                    # Add duration calculation logic here
                    pass
        
        # Calculate total experience
        if not result.get('total_experience_months') and result.get('work_experience'):
            total_months = PostProcessor.calculate_duration_months(result['work_experience'])
            result['total_experience_months'] = total_months
        
        # Standardize GPA
        if result.get('education'):
            for edu in result['education']:
                if edu.get('gpa'):
                    edu['gpa'] = PostProcessor.standardize_gpa(edu['gpa'])
        
        return result
