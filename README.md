# Job Application Agent

Automated job application assistant that generates personalized cover letters based on job descriptions and your resume.

## Features

- **Webpage Reading**: Extract job descriptions from URLs
- **Text Processing**: Analyze and summarize job requirements
- **Cover Letter Generation**: Create tailored LaTeX cover letters
- **PDF Conversion**: Compile LaTeX to PDF (requires LaTeX installation)

## Modules

### Core Modules
1. `local_cover_letter_generator.py` - Main script for generating cover letters
2. `webpage_reader.py` - Extracts job descriptions from web pages
3. `read_jd.py` - Processes text job descriptions
4. `deep_seek_api.py` - Interface for AI text generation
5. `prompts.py` - Contains prompt templates for cover letter generation

### Template Files
- `cover_letter_template/` - LaTeX template files (main.tex, body.tex, info.tex)

## Usage

### From Web URL
```bash
python local_cover_letter_generator.py --url "JOB_POSTING_URL" [--pdf]
```

### From Text File
```bash
python local_cover_letter_generator.py --file "job_description.txt" [--pdf]
```

Options:
- `--pdf`: Generate PDF (requires pdflatex)
- `--output`: Custom output folder name
- `--use-ollama`: Use local Ollama instead of DeepSeek API
- `--model`: Specify Ollama model name

## Requirements
- Python 3.x
- Required packages: `requests`, `ollama`
- For PDF generation: LaTeX distribution (MacTeX, TeX Live, or MiKTeX)

## Output
Generated cover letters are saved in `cover_letter_[JOB_NAME]` folders containing:
- LaTeX source files
- Generated PDF (if --pdf option used)
