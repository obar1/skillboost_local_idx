import requests
from loguru import logger as logging
from pathlib import Path
from typing import Union

HTTPS_SKILL_BOOST = "https://cloudskillsboost.google"


def fetch_page(template_type: str, template_id: Union[int, str]) -> str:
    url = f"{HTTPS_SKILL_BOOST}/{template_type}/{template_id}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as http_err:
        logging.info(
            f"HTTP error occurred: {http_err} - Status code: {response.status_code}"
        )
        raise
    except requests.RequestException as err:
        logging.info(f"Error fetching the page: {err}")
        raise


def save_html(
    template_type: str,
    template_id: Union[int, str],
    html_content: str,
    output_path: Path,
    only_valid_results: bool,
) -> None:
    url = f"{HTTPS_SKILL_BOOST}/{template_type}/{template_id}"
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
        raise Exception(
            "Warning: Page may be protected by reCAPTCHA. PDF conversion might not work properly."
        )
    output_path.write_text(full_html, encoding="utf-8")
    logging.info(f"Page saved successfully as '{output_path}'")


def generate_pdf(input_html_path: Path, only_valid_results: bool) -> Path:
    from weasyprint import HTML
    from reportlab.pdfgen import canvas

    output_pdf_path = input_html_path.with_suffix(".html.pdf")
    try:
        HTML(input_html_path).write_pdf(output_pdf_path)
        logging.info(f"PDF saved to: {output_pdf_path}")
        input_html_path.unlink()
        logging.info(f"Deleted HTML file: {input_html_path}")
    except Exception:
        if only_valid_results:
            logging.info(
                f"PDF generation skipped for {input_html_path}, only_valid_results {only_valid_results}."
            )
            return None

        # Create an empty PDF as fallback
        try:
            from io import BytesIO

            buffer = BytesIO()
            c = canvas.Canvas(buffer)
            c.drawString(
                100,
                750,
                f"PDF generation failed. This is a placeholder for {input_html_path},  only_valid_results is {only_valid_results}.",
            )
            c.save()
            with open(output_pdf_path, "wb") as f:
                f.write(buffer.getvalue())
            logging.info(f"Empty placeholder PDF created at: {output_pdf_path}")
        except Exception as fallback_error:
            logging.info(f"Failed to create fallback PDF: {fallback_error}")
            raise

    return output_pdf_path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch Google Skills Boost course template and save as HTML/PDF."
    )
    parser.add_argument("template_type", type=str, help="Course Template Type to fetch")
    parser.add_argument("template_id", type=int, help="Course Template ID to fetch")
    parser.add_argument(
        "--output_dir", default="./.pdf", help="Directory to save HTML/PDF"
    )
    parser.add_argument(
        "--only_valid_results", dest="only_valid_results", action="store_true"
    )
    parser.add_argument(
        "--allow_invalid_results", dest="only_valid_results", action="store_false"
    )
    parser.set_defaults(only_valid_results=False)

    args = parser.parse_args()
    logging.info(f"input args {args}")

    try:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        html_path = output_dir / f"{args.template_type}{args.template_id}.html"
        only_valid_results = args.only_valid_results
        if html_path.exists():
            logging.info(
                f"File '{html_path}' already exists. Skipping download and PDF generation."
            )
            return

        html_content = fetch_page(args.template_type, args.template_id)
        save_html(
            args.template_type,
            args.template_id,
            html_content,
            html_path,
            only_valid_results,
        )
    except Exception as e:
        logging.info(f"Failed: {e}")
    finally:
        generate_pdf(html_path, only_valid_results)


if __name__ == "__main__":
    main()
