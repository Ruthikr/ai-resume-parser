"""
Batch processing example for ResumeParser Pro
"""

from resumeparser_pro import ResumeParserPro
import json

# Initialize parser with more workers for faster processing
parser = ResumeParserPro(
    provider="google_genai",
    model_name="gemini-2.0-flash",
    api_key="your-api-key-here",
    max_workers=10  # Process 10 resumes in parallel
)

# Process multiple resumes
file_paths = ["resume1.pdf", "resume2.docx", "resume3.pdf"]
results = parser.parse_batch(file_paths)

# Get only successful results
successful_resumes = parser.get_successful_resumes(results)

# Print summary
summary = parser.get_summary(results)
print(f"Success Rate: {summary['success_rate']:.1f}%")
print(f"Total Time: {summary['total_processing_time']:.2f}s")
print(f"Average Time: {summary['avg_processing_time']:.2f}s per resume")

# Save batch results
with open("batch_results.json", "w") as f:
    json.dump(successful_resumes, f, indent=2)

print(f"Successfully parsed {len(successful_resumes)} resumes")
