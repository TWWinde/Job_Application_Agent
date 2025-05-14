import requests
from bs4 import BeautifulSoup
import os
import json
import re
from datetime import datetime
from deep_seek_api import deepseek_api
from prompts import cover_letter_prompt
from read_jd import read_txt_as_single_line

def read_webpage(url):
    """
    Read the content of a webpage.

    Args:
        url (str): The URL of the webpage to read.

    Returns:
        str: The content of the webpage.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # Set encoding to UTF-8
        return response.text
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return None

def extract_job_description(html_content):
    """
    Extract job description from HTML content using BeautifulSoup.
    
    Args:
        html_content (str): HTML content of the webpage.
        
    Returns:
        str: Extracted job description.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Common job description selectors
    job_description = ""
    
    # Try different common selectors for job descriptions
    selectors = [
        # Common job description containers
        "div.job-description", "div.description", "div.jobDescriptionText",
        "div[data-automation='jobDescription']", "div.job_description",
        "section#job-description", "div#job-details", "div.details",
        "div.job-details", "div.vacancy-description", "div.content",
        "div.job-info", "div.job-overview", "div.job-summary",
        # LinkedIn specific
        "div.description__text", "section.description",
        # Indeed specific
        "div#jobDescriptionText", "div.jobsearch-jobDescriptionText",
        # Glassdoor specific
        "div.jobDescriptionContent", "div.desc",
        # Academic job boards
        "div.job-description-container", "div.job-posting-body",
        # Generic content areas
        "article", "main", "div.main-content"
    ]
    
    # Try each selector
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            for element in elements:
                job_description += element.get_text(strip=True) + " "
            if job_description.strip():
                break
    
    # If no specific job description container found, try to find by keywords
    if not job_description.strip():
        # Look for headers that might indicate job description sections
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b'])
        for header in headers:
            header_text = header.get_text(strip=True).lower()
            if any(keyword in header_text for keyword in ['job description', 'about the role', 'about the job', 'position details', 'responsibilities', 'requirements']):
                # Get the content following this header
                content = []
                for sibling in header.find_next_siblings():
                    # Stop if we hit another header or a clearly different section
                    if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] or \
                       any(keyword in sibling.get_text(strip=True).lower() for keyword in ['apply now', 'about the company', 'about us']):
                        break
                    content.append(sibling.get_text(strip=True))
                
                if content:
                    job_description += " ".join(content) + " "
    
    # If still no job description, get all text from the page and try to extract relevant parts
    if not job_description.strip():
        all_text = soup.get_text(strip=True)
        
        # Look for common job description patterns
        patterns = [
            r"(?:Job Description|Position Description|Role Description).*?(?:Requirements|Qualifications|About You|About the Company|Apply Now)",
            r"(?:Responsibilities|What You'll Do|The Role).*?(?:Requirements|Qualifications|Skills|Experience|Education)",
            r"(?:About the Role|About the Position).*?(?:Requirements|Qualifications|What You Bring|What You'll Need)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, all_text, re.IGNORECASE | re.DOTALL)
            if match:
                job_description = match.group(0)
                break
    
    # Clean up the text
    if job_description:
        # Remove extra whitespace
        job_description = re.sub(r'\s+', ' ', job_description).strip()
        
        # Remove common boilerplate text
        boilerplate_phrases = [
            "Please apply online", "Apply now", "Click to apply",
            "Submit your application", "Submit your resume",
            "Equal opportunity employer", "We are an equal opportunity employer"
        ]
        
        for phrase in boilerplate_phrases:
            job_description = job_description.replace(phrase, "")
    
    return job_description.strip() if job_description else "Could not extract job description from the provided URL."

def save_job_description(job_description, job_title=None):
    """
    Save the job description to a text file.
    
    Args:
        job_description (str): The job description to save.
        job_title (str, optional): The title of the job. If None, a timestamp will be used.
        
    Returns:
        str: The path to the saved file.
    """
    # Create job_txt directory if it doesn't exist
    if not os.path.exists('job_txt'):
        os.makedirs('job_txt')
    
    # Generate filename
    if job_title:
        # Clean the job title to make it suitable for a filename
        job_title = re.sub(r'[^\w\s-]', '', job_title).strip()
        job_title = re.sub(r'[-\s]+', '-', job_title)
    else:
        # Use timestamp if no job title is provided
        job_title = f"job-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    file_path = f"job_txt/{job_title}.txt"
    
    # Save the job description
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(job_description)
    
    # Update work_info.json
    try:
        if os.path.exists('work_info.json'):
            with open('work_info.json', 'r', encoding='utf-8') as file:
                work_info = json.load(file)
        else:
            work_info = {}
        
        # Add the new job description
        work_info[job_title] = job_description
        
        # Save the updated work_info.json
        with open('work_info.json', 'w', encoding='utf-8') as file:
            json.dump(work_info, file, indent=4)
    except Exception as e:
        print(f"Error updating work_info.json: {e}")
    
    return file_path

def extract_job_title(html_content, url):
    """
    Extract job title from HTML content.
    
    Args:
        html_content (str): HTML content of the webpage.
        url (str): URL of the webpage (used as fallback for title extraction).
        
    Returns:
        str: Extracted job title or None if not found.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find job title in common locations
    # 1. Look for title in meta tags
    meta_title = soup.find('meta', property='og:title') or soup.find('meta', attrs={'name': 'title'})
    if meta_title and meta_title.get('content'):
        return meta_title['content']
    
    # 2. Look for title in common job title elements
    title_selectors = [
        "h1.job-title", "h1.jobTitle", "h1.title", "h1.posting-headline",
        "h1.job-header__title", "h1.job-headline", "h1.job-details-title",
        "h1", "h2.job-title", "h2.title", ".job-title", ".jobTitle",
        ".position-title", ".listing-title", ".job-header-title"
    ]
    
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            return title_elem.get_text(strip=True)
    
    # 3. Look for title in page title
    if soup.title:
        title_text = soup.title.get_text(strip=True)
        # Try to clean up the title (remove company name, website name, etc.)
        title_parts = re.split(r'[-|]', title_text)
        if title_parts:
            return title_parts[0].strip()
    
    # 4. Extract from URL as last resort
    if url:
        # Try to extract meaningful parts from the URL
        url_parts = url.split('/')
        for part in url_parts:
            if len(part) > 5 and '-' in part:  # Likely a slug with job title
                return part.replace('-', ' ').title()
    
    return "Job Position"  # Default fallback

def generate_latex_cover_letter(job_description, output_file=None):
    """
    Generate a LaTeX cover letter based on the job description.
    
    Args:
        job_description (str): The job description.
        output_file (str, optional): The path to save the LaTeX file. If None, a default name will be used.
        
    Returns:
        str: The path to the generated LaTeX file.
    """
    # Generate the prompt for the cover letter
    prompt = cover_letter_prompt(job_description)
    
    # Generate the cover letter using DeepSeek API
    cover_letter_content = deepseek_api(prompt)
    
    # If no output file specified, create one
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        output_file = f"cover_letter_{timestamp}.tex"
    
    # Save the LaTeX cover letter
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cover_letter_content)
    
    return output_file

def process_job_url(url):
    """
    Process a job URL: read the webpage, extract job description and title,
    save the job description, and generate a LaTeX cover letter.
    
    Args:
        url (str): The URL of the job posting.
        
    Returns:
        tuple: (job_description_path, cover_letter_path) - Paths to the saved files.
    """
    # Read the webpage
    html_content = read_webpage(url)
    if not html_content:
        print("Failed to read the webpage.")
        return None, None
    
    # Extract job title and description
    job_title = extract_job_title(html_content, url)
    job_description = extract_job_description(html_content)
    
    if not job_description or job_description == "Could not extract job description from the provided URL.":
        print("Failed to extract job description.")
        return None, None
    
    # Save the job description
    job_description_path = save_job_description(job_description, job_title)
    
    # Generate LaTeX cover letter
    cover_letter_path = generate_latex_cover_letter(job_description, f"cover_letter_{job_title.replace(' ', '_')}.tex")
    
    return job_description_path, cover_letter_path

if __name__ == "__main__":
    # Example usage
    url = input("Enter the job posting URL: ")
    job_description_path, cover_letter_path = process_job_url(url)
    
    if job_description_path and cover_letter_path:
        print(f"Job description saved to: {job_description_path}")
        print(f"Cover letter generated at: {cover_letter_path}")
    else:
        print("Failed to process the job URL.")
