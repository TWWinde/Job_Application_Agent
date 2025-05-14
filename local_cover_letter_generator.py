
import requests
import json
import argparse
import os
import shutil
from ollama import chat
from ollama import ChatResponse
from webpage_reader import process_job_url
from read_jd import read_txt_as_single_line
from prompts import cover_letter_prompt
from deep_seek_api import deepseek_api

def get_request(model_name, prompt):
    """
    Generate a response from the Ollama model running locally.

    Args:
        model_name (str): The name of the local Ollama model (e.g., "llama2", "mistral").
        prompt (str): The input prompt for the model.

    Returns:
        str: The generated text response from the model.
    """
    response: ChatResponse = chat(model=model_name, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    res = json.loads(response.model_dump_json())
    ans = res["message"]["content"]
    return ans

def generate_cover_letter_from_file(jd_file_path, output_file=None, use_ollama=False, model_name="deepseek-r1:8b"):
    """
    Generate a cover letter from a job description file using template structure.
    
    Args:
        jd_file_path (str): Path to the job description file.
        output_file (str, optional): Path to save the LaTeX folder. If None, a default name will be used.
        use_ollama (bool): Whether to use Ollama model instead of DeepSeek API.
        model_name (str): The name of the Ollama model to use if use_ollama is True.
        
    Returns:
        str: The path to the generated LaTeX folder.
    """
    # Read the job description
    jd = read_txt_as_single_line(jd_file_path)
    
    # Generate the prompt for body content
    prompt = cover_letter_prompt(jd)
    
    # Generate the body content
    if use_ollama:
        body_content = get_request(model_name, prompt)
    else:
        body_content = deepseek_api(prompt)
    
    # Create output folder with template structure
    if not output_file:
        base_name = os.path.basename(jd_file_path)
        file_name = os.path.splitext(base_name)[0]
        output_folder = f"cover_letter_{file_name}"
    else:
        output_folder = output_file
    
    os.makedirs(output_folder, exist_ok=True)
    
    # Copy template files
    template_dir = "cover_letter_template"
    for item in os.listdir(template_dir):
        src = os.path.join(template_dir, item)
        dst = os.path.join(output_folder, item)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    
    # Update body.tex with generated content
    body_path = os.path.join(output_folder, "body.tex")
    with open(body_path, 'w', encoding='utf-8') as file:
        file.write(body_content)
    
    # TODO: Update info.tex based on job description
    
    return output_folder

def compile_latex_to_pdf(folder_path):
    """
    Compile the LaTeX files in the folder to PDF.
    
    Args:
        folder_path (str): Path to the folder containing LaTeX files.
        
    Returns:
        str: Path to the generated PDF file.
    """
    try:
        # Check if pdflatex is available
        if os.system('which pdflatex > /dev/null 2>&1') != 0:
            print("\nWarning: pdflatex not found. Please install a LaTeX distribution like:")
            print("  - Mac: BasicTeX or MacTeX (https://www.tug.org/mactex/)")
            print("  - Linux: texlive (sudo apt install texlive-latex-base)")
            print("  - Windows: MiKTeX (https://miktex.org/)")
            print("LaTeX files are still available in the folder for manual compilation.")
            return None
            
        # Change to the folder and compile main.tex
        original_dir = os.getcwd()
        os.chdir(folder_path)
        os.system('pdflatex -interaction=nonstopmode main.tex')
        os.chdir(original_dir)
        
        pdf_path = os.path.join(folder_path, 'main.pdf')
        if os.path.exists(pdf_path):
            return pdf_path
        return None
    except Exception as e:
        print(f"Error compiling LaTeX to PDF: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate a cover letter from a job description.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='URL of the job posting')
    group.add_argument('--file', type=str, help='Path to the job description file')
    parser.add_argument('--output', type=str, help='Path to save the LaTeX folder')
    parser.add_argument('--use-ollama', action='store_true', help='Use Ollama model instead of DeepSeek API')
    parser.add_argument('--model', type=str, default="deepseek-r1:8b", help='Model name for Ollama (default: deepseek-r1:8b)')
    parser.add_argument('--pdf', action='store_true', help='Compile LaTeX to PDF after generation')
    
    args = parser.parse_args()
    
    if args.url:
        # Process the job URL
        job_description_path, cover_letter_path = process_job_url(args.url)
        
        if job_description_path and cover_letter_path:
            print(f"Job description saved to: {job_description_path}")
            print(f"Cover letter generated at: {cover_letter_path}")
            
            if args.pdf:
                pdf_path = compile_latex_to_pdf(cover_letter_path)
                if pdf_path:
                    print(f"PDF generated at: {pdf_path}")
        else:
            print("Failed to process the job URL.")
    
    elif args.file:
        # Generate cover letter from file
        output_file = args.output
        cover_letter_folder = generate_cover_letter_from_file(
            args.file, 
            output_file, 
            use_ollama=args.use_ollama, 
            model_name=args.model
        )
        
        print(f"Cover letter generated at: {cover_letter_folder}")
        
        if args.pdf:
            pdf_path = compile_latex_to_pdf(cover_letter_folder)
            if pdf_path:
                print(f"PDF generated at: {pdf_path}")

if __name__ == "__main__":
    main()
