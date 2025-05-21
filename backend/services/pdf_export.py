from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
import cairosvg

class PDFExporter:
    def generate_pdf(self, svg_content: str, output_path: str) -> str:
        # Convert SVG to PDF
        pdf_buffer = BytesIO()
        cairosvg.svg2pdf(bytestring=svg_content.encode('utf-8'), write_to=pdf_buffer)
        
        # Create PDF with ReportLab
        c = canvas.Canvas(output_path, pagesize=letter)
        c.drawString(72, 800, "System Architecture Diagram")
        c.drawImage(ImageReader(pdf_buffer), 72, 300, width=450, height=450)
        c.save()
        
        return output_path
