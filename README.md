# ResumeParser Pro 🚀

[![PyPI version](https://badge.fury.io/py/ai-resume-parser.svg)](https://badge.fury.io/py/resumeparser-pro)
[![Python Support](https://img.shields.io/pypi/pyversions/ai-resume-parser.svg)](https://pypi.org/project/resumeparser-pro/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready AI-powered resume parser with parallel processing capabilities. Extract structured data from resumes in PDF, DOCX, and TXT formats using state-of-the-art language models.

## 🌟 Features

- **🤖 AI-Powered**: Uses advanced language models (GPT, Gemini, Claude, etc.)
- **⚡ Parallel Processing**: Process multiple resumes simultaneously
- **📊 Structured Output**: Returns clean, validated JSON data
- **🎯 High Accuracy**: Extracts 20+ fields with intelligent categorization
- **📈 Production Ready**: Robust error handling and logging
- **🔌 Easy Integration**: Simple API with just 3 lines of code

## 🚀 Quick Start

### Installation
```bash
pip install ai-resume-parser
```
For full functionality (recommended)
```bash
pip install ai-resume-parser[full]
```


### Basic Usage
```python
from resumeparser_pro import ResumeParserPro

#Initialize parser
parser = ResumeParserPro(
provider="google_genai",
model_name="gemini-2.0-flash",
api_key="your-api-key"
)

#Parse single resume
result = parser.parse_resume("resume.pdf")
print(f"Name: {result.resume_data.contact_info.full_name}")
print(f"Experience: {result.resume_data.total_experience_months} months")
```
#Example Parsed Resume data
```python
{'file_path': '/content/Stockholm-Resume-Template-Simple.pdf',
 'success': True,
 'resume_data': {'contact_info': {'full_name': 'Jason Miller',
   'email': 'email@email.com',
   'phone': '+13868683442',
   'location': 'Los Angeles, CA 90291, United States',
   'linkedin': 'https://www.linkedin.com/in/jason-miller',
   'github': None,
   'portfolio': None,
   'other_profiles': ['https://www.pinterest.com/jason-miller']},
  'professional_summary': 'Experienced Amazon Associate with five years’ tenure in a shipping yard setting, maintaining an average picking/packing speed of 98%. Holds a zero error% score in adhering to packing specs and 97% error-free ratio on packing records. Completed a certificate in Warehouse Sanitation and has a valid commercial driver’s license.',
  'skills': [{'category': 'Technical Skills',
    'skills': ['Picking',
     'Packing',
     'Inventory Management',
     'Shipping',
     'Record Keeping',
     'Kanban System',
     'Kaizen',
     'Gemba',
     '5S'],
    'proficiency_level': None},
   {'category': 'Soft Skills',
    'skills': ['Mathematics'],
    'proficiency_level': None},
   {'category': 'Other',
    'skills': ['Cleaning Equipment', 'Deep Sanitation Practices'],
    'proficiency_level': None}],
  'work_experience': [{'job_title': 'Amazon Warehouse Associate',
    'company': 'Amazon',
    'location': 'Miami Gardens',
    'employment_type': None,
    'start_date': '2021-01',
    'end_date': '2022-07',
    'duration_months': 19,
    'description': 'Performed all warehouse laborer duties such as packing, picking, counting, record keeping, and maintaining a clean area.',
    'responsibilities': [],
    'achievements': ['Consistently maintained picking/packing speeds in the 98th percentile.',
     'Picked all orders with 100% accuracy despite high speeds.',
     'Maintained a clean work area, meeting 97.5% of the inspection requirements.'],
    'technologies': []},
   {'job_title': 'Laboratory Inventory Assistant',
    'company': 'Dunrea Laboratories',
    'location': 'Orlando',
    'employment_type': 'Full-time',
    'start_date': '2019-01',
    'end_date': '2020-12',
    'duration_months': 24,
    'description': 'Full-time lab assistant in a small, regional laboratory tasked with · participating in Kaizen Events, Gemba walks, and 5S to remove barriers and improve productivity.',
    'responsibilities': ['Filled the warehouse helper job description, which involved picking, packing, shipping, inventory management, and cleaning equipment.'],
    'achievements': ['Saved 12% on UPS orders by staying on top of special deals.',
     'Cut down storage waste by 23% by switching to a Kanban system.'],
    'technologies': []}],
  'education': [{'degree': 'Associates Degree in Logistics and Supply Chain Fundamentals',
    'field_of_study': None,
    'institution': 'Atlanta Technical College',
    'location': 'Atlanta',
    'start_date': '2021-01',
    'end_date': '2022-07',
    'gpa': None,
    'honors': [],
    'relevant_coursework': ['Warehousing Operations',
     'Logistics and Distribution Practices',
     'Inventory Systems',
     'Supply Chain Principles']}],
  'projects': [],
  'certifications': [],
  'languages': [{'language': 'English', 'proficiency': None},
   {'language': 'Spanish', 'proficiency': None}],
  'publications': [],
  'awards': [{'title': 'Employee of the month',
    'issuer': 'Amazon',
    'date': None,
    'description': None}],
  'volunteer_experience': [],
  'interests': ['Action Cricket', 'Rugby', 'Athletics'],
  'total_experience_months': 43,
  'industry': 'Logistics & Supply Chain',
  'seniority_level': 'Mid-level'},
 'error_message': None,
 'parsing_time_seconds': 18.71349,
 'timestamp': '2025-07-25T15:19:50.614831'}
```

# Flexible approach (recommended)
```python
if result.success:
    name = result.resume_data.contact_info.full_name
    experience = result.resume_data.total_experience_months
    
# Quick overview (convenience method)
print(result.get_summary())

# Full data export
resume_dict = result.model_dump()
```

### Batch Processing
```python
#Process multiple resumes in parallel
file_paths = ["resume1.pdf", "resume2.docx", "resume3.pdf"]
results = parser.parse_batch(file_paths)
#returns list of parsed resumes

#Get successful results
successful_resumes = parser.get_successful_resumes(results)
print(f"Parsed {len(successful_resumes)} resumes successfully")
```

## 📊 Extracted Data

ResumeParser Pro extracts **20+ structured fields**:

### Contact Information
- Full name, email, phone number
- Location, LinkedIn, GitHub, portfolio
- Other social profiles

### Professional Data
- Work experience with **integer month durations**
- Education with GPA standardization
- Skills categorized by type
- Projects with technologies and outcomes
- Certifications with dates and organizations

### Metadata
- Total experience in months
- Industry classification
- Seniority level assessment

## 🎯 Supported AI Providers

Since `ai-resume-parser` uses LangChain's `init_chat_model`, it supports **all LangChain-compatible providers**:

### **Major Providers:**
| Provider | Example Models | Setup |
|----------|--------|-------|
| **Google** | Gemini 2.0 Flash, Gemini Pro, Gemini 1.5 | `provider="google_genai"` |
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-4 Turbo | `provider="openai"` |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | `provider="anthropic"` |
| **Azure OpenAI** | GPT-4, GPT-3.5-turbo | `provider="azure_openai"` |
| **AWS Bedrock** | Claude, Llama, Titan | `provider="bedrock"` |
| **Cohere** | Command, Command-R | `provider="cohere"` |
| **Mistral** | Mistral Large, Mixtral | `provider="mistral"` |
| **Ollama** | Local models (Llama, CodeLlama) | `provider="ollama"` |
| **Together** | Various open-source models | `provider="together"` |

### **Usage Examples:**
```python
#Google Gemini
!pip install langchain-google-genai

parser = ResumeParserPro(
provider="google_genai",
model_name="gemini-2.0-flash",
api_key="your-google-api-key"
)

#Azure OpenAI
parser = ResumeParserPro(
provider="azure_openai",
model_name="gpt-4",
api_key="your-azure-key"
)

#Local Ollama
parser = ResumeParserPro(
provider="ollama",
model_name="llama2:7b",
api_key="" # No API key needed for local
)

#AWS Bedrock
parser = ResumeParserPro(
provider="bedrock",
model_name="anthropic.claude-3-sonnet-20240229-v1:0",
api_key="your-aws-credentials"
)
```

**Full list**: See [LangChain Model Providers](https://python.langchain.com/docs/integrations/chat/) for complete provider support.


## 📈 Performance

- **Speed**: ~5-10 seconds per resume (based on th llm used)
- **Parallel Processing**: 5-10x faster for batch operations
- **Accuracy**: 95%+ field extraction accuracy
- **File Support**: PDF, DOCX, TXT formats

## 🛠️ Advanced Features

### Custom Configuration
```python
parser = ResumeParserPro(
provider="openai",
model_name="gpt-4o-mini",
api_key="your-api-key",
max_workers=10, # Parallel processing workers
temperature=0.1 # Model consistency
)
```

### Error Handling
```python
results = parser.parse_batch(file_paths, include_failed=True)

Get processing summary
summary = parser.get_summary(results)
print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Failed files: {len(summary['failed_files'])}")
```

## 📋 Requirements

- Python 3.8+
- API key from supported provider
- Optional: PyMuPDF, python-docx for enhanced file support

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- 📖 [Documentation](https://github.com/Ruthikr/ai-resume-parser/docs)
- 🐛 [Issue Tracker](https://github.com/Ruthikr/ai-resume-parser/issues)
- 💬 [Discussions](https://github.com/Ruthikr/ai-resume-parser/discussions)

---

**Built with ❤️ for the recruitment and HR community**
