import io
import logging

try:
    from xhtml2pdf import pisa
    XHTML2PDF_INSTALLED = True
except ImportError:
    XHTML2PDF_INSTALLED = False

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not XHTML2PDF_INSTALLED:
        raise ImportError("xhtml2pdf is not installed. PDF generation unavailable.")

    combined_body_parts = []
    for name, html_str in html_docs.items():
        combined_body_parts.append(
            f'<div style="page-break-after: always;">{html_str}</div>'
        )

    combined_html = '\n'.join(combined_body_parts)

    output = io.BytesIO()
    result = pisa.CreatePDF(src=combined_html, dest=output)

    if result.err:
        raise RuntimeError(f'xhtml2pdf failed to generate PDF (err code {result.err})')

    return output.getvalue()