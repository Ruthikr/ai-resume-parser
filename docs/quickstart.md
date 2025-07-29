# Quickstart Guide

This guide will walk you through the basic steps to parse a resume using **ResumeParser Pro**.

### 1. Initialize the Parser

First, import and initialize the `ResumeParserPro` class. You'll need to provide three key things:
1.  The AI `provider` (e.g., `"openai"`, `"google_genai"`).
2.  The `model_name` (e.g., `"gpt-4o-mini"`, `"gemini-1.5-pro"`).
3.  Your `api_key` for that provider.

from resumeparser_pro import ResumeParserPro

parser = ResumeParserPro(
provider="openai",
model_name="gpt-4o-mini",
api_key="sk-..." # Your OpenAI API Key
)

### 2. Parse a Single Resume

Use the `parse_resume()` method to process a single file. It supports various formats like PDF, DOCX, and even PNG or JPG files if you installed the `[ocr]` extra.

Path to the resume file
resume_path = "path/to/my_resume.pdf"

Parse the file
result = parser.parse_resume(resume_path)

The result object contains all the information
if result.success:
print("Parsing was successful!")

# Access the structured data
contact_info = result.resume_data.contact_info
experience = result.resume_data.work_experience

print(f"Candidate Name: {contact_info.full_name}")
print(f"Email: {contact_info.email}")
print(f"Total Experience: {result.resume_data.total_experience_months} months")

# Print the first job title
if experience:
    print(f"Latest Job: {experience.job_title} at {experience.company}")
else:
print(f"Parsing failed. Error: {result.error_message}")

### 3. Parse Multiple Resumes in a Batch

For handling multiple files, the `parse_batch()` method is highly efficient as it processes files in parallel.

file_paths = [
"resumes/resume_of_dev1.pdf",
"resumes/resume_of_dev2.docx",
"resumes/scanned_resume_of_dev3.png"
]

Process the entire batch
batch_results = parser.parse_batch(file_paths)

print(f"Processed {len(batch_results)} resumes.")

You can easily filter for successful results
successful_parses = [res for res in batch_results if res.success]

for parsed_resume in successful_parses:
print(f"Successfully parsed: {parsed_resume.file_path}")
print(f" - Name: {parsed_resume.resume_data.contact_info.full_name}\n")
undefined