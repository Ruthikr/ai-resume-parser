# ResumeParser Pro 🚀

[![PyPI version](https://badge.fury.io/py/ai-resume-parser.svg)](https://pypi.org/project/ai-resume-parser/1.0.6/)
[![Python Support](https://img.shields.io/pypi/pyversions/ai-resume-parser.svg)](https://pypi.org/project/ai-resume-parser/1.0.6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Production-ready AI-powered resume parser with parallel processing capabilities. Extract structured data from resumes in **PDF, DOCX, TXT, images (PNG, JPG), HTML, and ODT** formats using state-of-the-art language models.

## 🌟 Features

-   **🤖 AI-Powered**: Uses advanced language models (GPT, Gemini, Claude, etc.) for high-accuracy extraction.
-   **⚡ Parallel Processing**: Process multiple resumes simultaneously, significantly speeding up bulk operations.
-   **📊 Structured Output**: Returns clean, Pydantic-validated JSON data for easy integration.
-   **🎯 High Accuracy**: Extracts over 20 distinct fields, including categorized skills and work duration in months.
-   **📁 Multi-Format Support**: Natively handles PDF, DOCX, and TXT, with optional support for images (OCR), HTML, and ODT files.
-   **📈 Production Ready**: Features robust error handling, logging, and clear, structured results.
-   **🔌 Easy Integration**: A simple and intuitive API gets you started in just a few lines of code.

## 🚀 Quick Start

### Installation

For core functionality (PDF, DOCX, TXT), install the base package:
```bash
pip install ai-resume-parser
```

For full functionality, including support for images, HTML, and ODT files (recommended):
```bash
pip install ai-resume-parser[full]
```

See the "Supported File Formats" section for more specific installation options.

### Basic Usage

It only takes a few lines to parse your first resume.

```python
from resumeparser_pro import ResumeParserPro

# Initialize the parser with your chosen AI provider and API key
parser = ResumeParserPro(
    provider="google_genai",
    model_name="gemini-2.0-flash", # Or "gpt-4o-mini", "claude-3-5-sonnet", etc.
    api_key="your-llm-provider-api-key"
)
```

```python
# Parse a single resume file
# Supports .pdf, .docx, .txt, .png, .jpg, and more
result = parser.parse_resume("path/to/your/resume.pdf")

# Check if parsing was successful and access the data
if result.success:
    print(f"✅ Resume parsed successfully!")
    print(f"Name: {result.resume_data.contact_info.full_name}")
    print(f"Total Experience: {result.resume_data.total_experience_months} months")
    print(f"Industry: {result.resume_data.industry}")

    # You can also get a quick summary
    # print(result.get_summary()) # Assuming you add this convenience method

    # Or export the full data to a dictionary
    # resume_dict = result.model_dump()
else:
    print(f"❌ Parsing failed: {result.error_message}")
```

### Batch Processing

Process multiple resumes in parallel for maximum speed.

```python
# Process multiple resumes at once
file_paths = ["resume1.pdf", "resume2.docx", "scanned_resume.png"]
results = parser.parse_batch(file_paths)
```

```python
# Filter for only the successfully parsed resumes
successful_resumes = parser.get_successful_resumes(results)
print(f"Successfully parsed {len(successful_resumes)} out of {len(file_paths)} resumes.")
```

## 📁 Supported File Formats

ResumeParser Pro supports a wide range of file formats. For formats beyond PDF, DOCX, and TXT, you need to install optional dependencies.

| Format          | Extensions               | Required Installation Command          |
|-----------------|--------------------------|----------------------------------------|
| **Core Formats**| `.pdf`, `.docx`, `.txt`  | `pip install ai-resume-parser`         |
| **Images (OCR)**| `.png`, `.jpg`, `.jpeg`  | `pip install ai-resume-parser[ocr]`    |
| **HTML**        | `.html`, `.htm`          | `pip install ai-resume-parser[html]`   |
| **OpenDocument**| `.odt`                   | `pip install ai-resume-parser[odt]`    |

**❗️ Important Note for Image Parsing:**
To parse images (`.png`, `.jpg`), you must have the **Google Tesseract OCR engine** installed on your system. This is a separate step from the `pip` installation.
*   [Tesseract Installation Guide](https://github.com/tesseract-ocr/tesseract/wiki)

## 📊 Example Parsed Resume Data

The parser returns a structured `ParsedResumeResult` object. The core data is in `result.resume_data`, which follows a detailed Pydantic schema.

```python
{
    'file_path': 'resume.pdf',
    'success': True,
    'resume_data': {
        'contact_info': {
            'full_name': 'Jason Miller',
            'email': 'email@email.com',
            'phone': '+1386862',
            'location': 'Los Angeles, CA 90291, United States',
            'linkedin': 'https://www.linkedin.com/in/jason-miller'
        },
        'professional_summary': 'Experienced Amazon Associate with five years’ tenure...',
        'skills': [
            {'category': 'Technical Skills', 'skills': ['Picking', 'Packing', 'Inventory Management']}
        ],
        'work_experience': [{
            'job_title': 'Amazon Warehouse Associate',
            'company': 'Amazon',
            'start_date': '2021-01',
            'end_date': '2022-07',
            'duration_months': 19,
            'description': 'Performed all warehouse laborer duties...',
            'achievements': ['Consistently maintained picking/packing speeds in the 98th percentile.']
        }],
        'education': [{
            'degree': 'Associates Degree in Logistics and Supply Chain Fundamentals',
            'institution': 'Atlanta Technical College'
        }],
        'total_experience_months': 43,
        'industry': 'Logistics & Supply Chain',
        'seniority_level': 'Mid-level'
    },
    'parsing_time_seconds': 3.71,
    'timestamp': '2025-07-25T15:19:50.614831'
}
```

## 🎯 Supported AI Providers

The library is built on LangChain, so it supports a vast ecosystem of LLM providers. Here are some of the most common ones:

| Provider        | Example Models                            | Setup                  |
|-----------------|-------------------------------------------|------------------------|
| **Google**      | `gemini-2.0-flash`, `gemini-1.5-pro`      | `provider="google_genai"`|
| **OpenAI**      | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`    | `provider="openai"`      |
| **Anthropic**   | `claude-3-5-sonnet-20240620`, `claude-3-opus` | `provider="anthropic"`   |
| **Azure OpenAI**| `gpt-4`, `gpt-35-turbo`                   | `provider="azure_openai"`|
| **AWS Bedrock** | Claude, Llama, Titan models               | `provider="bedrock"`     |
| **Ollama**      | Local models like `llama3`, `codellama`   | `provider="ollama"`      |

**Full list**: See the [LangChain Chat Model Integrations](https://python.langchain.com/v0.2/docs/integrations/chat/) for a complete list of supported providers and model names.

### Provider Usage Examples

```python
# Using OpenAI's GPT-4o-mini
parser = ResumeParserPro(provider="openai", model_name="gpt-4o-mini", api_key="your-openai-key")
```

```python
# Using a local model with Ollama (no API key needed)
parser = ResumeParserPro(provider="ollama", model_name="llama3:8b", api_key="NA")
```

```python
# Using Anthropic's Claude 3.5 Sonnet
parser = ResumeParserPro(provider="anthropic", model_name="claude-3-5-sonnet-20240620", api_key="your-anthropic-key")
```

## 🛠️ Advanced Configuration

You can customize the parser's behavior during initialization.

```python
parser = ResumeParserPro(
    provider="openai",
    model_name="gpt-4o-mini",
    api_key="your-api-key",
    max_workers=10,      # Increase for faster batch processing
    temperature=0.0,     # Set to 0.0 for maximum consistency
)
```

## 🤝 Contributing

Contributions are highly welcome! Please feel free to submit a pull request or open an issue for bugs, feature requests, or suggestions.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🆘 Support

-   📖 **Documentation**: Check the code and examples in this repository.
-   🐛 **Issue Tracker**: Report bugs or issues [here](https://github.com/Ruthikr/ai-resume-parser/issues).
-   💬 **Discussions**: Ask questions or share ideas in our [Discussions tab](https://github.com/Ruthikr/ai-resume-parser/discussions).

---

**Built with ❤️ for the recruitment and HR community.**


