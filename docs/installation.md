# Installation Guide

Installing **ResumeParser Pro** is straightforward. You can choose a core installation or install optional extras for extended file format support.

### Core Installation

The core library provides support for the most common resume formats: `.pdf`, `.docx`, and `.txt`.

pip install ai-resume-parser


### Full Installation (Recommended)

To enable all supported file formats, including images (OCR), HTML, and OpenDocument Text (ODT), install the `[full]` extra:


### Optional Extras

You can also install support for specific file types individually:

-   **For Image Parsing (OCR)**:
    ```
    pip install ai-resume-parser[ocr]
    ```
-   **For HTML Parsing**:
    ```
    pip install ai-resume-parser[html]
    ```
-   **For OpenDocument (ODT) Parsing**:
    ```
    pip install ai-resume-parser[odt]
    ```

### ❗️ Mandatory Requirement for Image Parsing

To parse images (`.png`, `.jpg`, etc.), you must have the **Google Tesseract OCR engine** installed on your system. The Python library `pytesseract` is just a wrapper for this engine.

-   **Windows**: Download the installer from the official [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) page.
-   **macOS (via Homebrew)**: `brew install tesseract`
-   **Linux (Debian/Ubuntu)**: `sudo apt-get install tesseract-ocr`

After installation, ensure the `tesseract` command is available in your system's PATH.
