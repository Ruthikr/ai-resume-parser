"""
Basic usage example for ResumeParser Pro
"""

from resumeparser_pro import ResumeParserPro
import json

# Initialize the parser
parser = ResumeParserPro(
    provider="google_genai",
    model_name="gemini-2.0-flash",
    api_key="your-api-key-here"
)

# Parse a single resume
result = parser.parse_resume("resume.pdf")

if result.success:
    print("✅ Resume parsed successfully!")
    print(f"Name: {result.resume_data.contact_info.full_name}")
    print(f"Total Experience: {result.resume_data.total_experience_months} months")
    print(f"Industry: {result.resume_data.industry}")
    
    # Save to JSON
    with open("parsed_resume.json", "w") as f:
        json.dump(result.resume_data.model_dump(), f, indent=2)
else:
    print(f"❌ Parsing failed: {result.error_message}")
