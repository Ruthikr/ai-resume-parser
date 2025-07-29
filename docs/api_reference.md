# API Reference

This section provides a detailed look at the classes, methods, and data structures available in **ResumeParser Pro**.

---

## `ResumeParserPro` Class

This is the main class for parsing resumes.

resumeparser_pro.ResumeParserPro(
provider: str,
model_name: str,
api_key: str,
max_workers: int = 5,
temperature: float = 0.1
)

### Initialization Parameters

| Parameter      | Type    | Description                                                                                                   |
|----------------|---------|---------------------------------------------------------------------------------------------------------------|
| `provider`     | `str`   | **Required**. The name of the LLM provider (e.g., `"openai"`, `"google_genai"`, `"anthropic"`, `"ollama"`).      |
| `model_name`   | `str`   | **Required**. The specific model to use (e.g., `"gpt-4o-mini"`, `"gemini-1.5-pro"`).                             |
| `api_key`      | `str`   | **Required**. Your API key for the specified provider. Use `"NA"` or an empty string for local providers like Ollama. |
| `max_workers`  | `int`   | The number of parallel threads to use for batch processing. Defaults to `5`.                                    |
| `temperature`  | `float` | The model's temperature for generation (0.0 for deterministic, >0 for creative). Defaults to `0.1`.            |

### Methods

#### `parse_resume()`
Parses a single resume file.

.parse_resume(file_path: Union[str, Path]) -> ParsedResumeResult

-   **file_path**: The local path to the resume file.
-   **Returns**: A `ParsedResumeResult` object containing the outcome.

#### `parse_batch()`
Parses a list of resume files in parallel.

.parse_batch(file_paths: List[Union[str, Path]]) -> List[ParsedResumeResult]
-   **file_paths**: A list of local paths to the resume files.
-   **Returns**: A list of `ParsedResumeResult` objects, one for each file.

#### `get_successful_resumes()`
A convenience method to filter a list of results from a batch job.

.get_successful_resumes(results: List[ParsedResumeResult]) -> List[Dict[str, Any]]
-   **results**: The list of `ParsedResumeResult` objects returned by `parse_batch()`.
-   **Returns**: A list of dictionaries, where each dictionary is the structured data of a successfully parsed resume.

---

## Data Models

The library uses Pydantic models to ensure that all output is structured and validated.

### `ParsedResumeResult` Model
This is the top-level wrapper for any parsing result.

| Field                  | Type            | Description                                                |
|------------------------|-----------------|------------------------------------------------------------|
| `file_path`            | `str`           | The path of the processed resume file.                     |
| `success`              | `bool`          | `True` if parsing was successful, `False` otherwise.       |
| `resume_data`          | `ResumeSchema`  | The structured resume data. `None` if parsing failed.      |
| `error_message`        | `str`           | The error message if parsing failed. `None` if successful. |
| `parsing_time_seconds` | `float`         | The total time taken to parse the file.                    |
| `timestamp`            | `str`           | The ISO 8601 timestamp of when the parsing finished.       |

### `ResumeSchema` Model
This model contains all the extracted fields from the resume.

| Field                     | Type               | Description                                           |
|---------------------------|--------------------|-------------------------------------------------------|
| `contact_info`            | `ContactInfo`      | The candidate's contact details.                      |
| `professional_summary`    | `str`              | The professional summary or objective statement.      |
| `skills`                  | `List[Skill]`      | A list of categorized skills.                         |
| `work_experience`         | `List[Experience]` | A list of work experiences.                           |
| `education`               | `List[Education]`  | A list of educational qualifications.                 |
| `projects`                | `List[Project]`    | A list of personal or professional projects.          |
| `certifications`          | `List[Certification]`| A list of certifications.                           |
| `languages`               | `List[Language]`   | A list of languages spoken by the candidate.          |
| `total_experience_months` | `int`              | The calculated total work experience in integer months.|
| `industry`                | `str`              | The primary industry of the candidate's experience.   |
| `seniority_level`         | `str`              | The assessed seniority level (e.g., "Junior", "Senior"). |
| *(and others...)*         |                    | `publications`, `awards`, `interests`, etc.           |

---
