import subprocess
import sys
import requests
import logging
import os
from pathlib import Path
from typing import Union

REPO_PREFIX = "course_templates_"
DEFAULT_WKHTMLTOPDF = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

logging.basicConfig(level=logging.INFO)

def fetch_page(template_id: Union[int, str]) -> str:
    """Fetches the HTML content for a Google Cloud Skills Boost course template."""
    url = f"https://partner.cloudskillsboost.google/course_templates/{template_id}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
        raise
    except requests.RequestException as err:
        logging.error(f"Error fetching the page: {err}")
        raise

def save_html(template_id: Union[int, str], html_content: str, output_path: Path) -> None:
    """Saves HTML content to a file, including a header with the source URL."""
    url = f"https://partner.cloudskillsboost.google/course_templates/{template_id}"
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Saved Course Template {template_id}</title>
</head>
<body>
    <p>Original page: <a href="{url}" target="_blank">{url}</a></p>
    <hr>
    {html_content}
</body>
</html>"""
    if "This site is protected by reCAPTCHA and the Google" in full_html:
        raise Exception("Warning: Page may be protected by reCAPTCHA. PDF conversion might not work properly.")
    output_path.write_text(full_html, encoding='utf-8')
    logging.info(f"Page saved successfully as '{output_path}'")

def generate_pdf(input_html_path: Path, wkhtmltopdf_path: str = DEFAULT_WKHTMLTOPDF) -> Path:
    """Converts an HTML file to PDF using wkhtmltopdf."""
    if not Path(wkhtmltopdf_path).exists():
        logging.error(f"wkhtmltopdf not found at: {wkhtmltopdf_path}")
        raise FileNotFoundError(f"wkhtmltopdf not found at: {wkhtmltopdf_path}")

    output_pdf_path = input_html_path.with_suffix('.html.pdf')
    try:
        subprocess.run([wkhtmltopdf_path, str(input_html_path), str(output_pdf_path)], check=True)
        logging.info(f"PDF saved to: {output_pdf_path}")
     # Delete HTML file after PDF is generated
        input_html_path.unlink()
        logging.info(f"Deleted HTML file: {input_html_path}")
        return output_pdf_path
    except subprocess.CalledProcessError as e:
        logging.error(f"PDF generation failed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Fetch Google Skills Boost course template and save as HTML/PDF.")
    parser.add_argument("template_id", type=int, help="Course Template ID to fetch")
    parser.add_argument("--wkhtmltopdf", default=os.getenv("WKHTMLTOPDF_PATH", DEFAULT_WKHTMLTOPDF), help="Path to wkhtmltopdf binary")
    parser.add_argument("--output-dir", default=".", help="Directory to save HTML/PDF")
    args = parser.parse_args()

    try:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        html_path = output_dir / f"{REPO_PREFIX}{args.template_id}.html"
        html_content = fetch_page(args.template_id)
        save_html(args.template_id, html_content, html_path)
        generate_pdf(html_path, args.wkhtmltopdf)
    except Exception as e:
        logging.error(f"Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()