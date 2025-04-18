"""
Reporting Module

This module provides functions for generating and exporting stock analysis reports.
"""

import os
import markdown2
import tempfile
from IPython.display import Markdown, display


class ReportGenerator:
    """Class for generating and exporting stock analysis reports."""

    def __init__(self):
        """Initialize the report generator."""
        pass
    
    @staticmethod
    def display_markdown(markdown_text):
        """
        Display formatted markdown in a notebook.
        
        Args:
            markdown_text (str): Markdown formatted text
        """
        display(Markdown(markdown_text))
    
    @staticmethod
    def export_report_to_pdf(report_text, symbol, filename=None):
        """
        Export the markdown report to a PDF file using FPDF.
        
        Args:
            report_text (str): Markdown formatted report text
            symbol (str): Stock symbol for the header
            filename (str, optional): Output filename. If None, uses 'stock_analysis_report.pdf'
            
        Returns:
            str: Path to the generated PDF file or error message
        """
        try:
            from fpdf import FPDF
            
            if filename is None:
                filename = f"{symbol}_analysis_report.pdf"
            
            class PDF(FPDF):
                def header(self):
                    # Set up the header with company name
                    self.set_font('Arial', 'B', 15)
                    self.cell(0, 10, f"{symbol} - Stock Analysis Report", 0, 1, 'C')
                    self.ln(10)
                
                def footer(self):
                    # Add a footer with page number
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
            # Create PDF instance
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            # Process the markdown content
            current_font_size = 12
            in_list = False
            
            for line in report_text.split('\n'):
                # Safely encode the line to avoid encoding issues
                line = line.encode('latin-1', 'replace').decode('latin-1')
                
                # Section headers
                if line.strip().startswith('# '):
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(0, 10, line.replace('#', '').strip(), ln=True)
                    pdf.ln(5)
                    current_font_size = 12
                elif line.strip().startswith('## '):
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(0, 10, line.replace('##', '').strip(), ln=True)
                    pdf.ln(3)
                    current_font_size = 12
                elif line.strip().startswith('### '):
                    pdf.set_font('Arial', 'B', 13)
                    pdf.cell(0, 10, line.replace('###', '').strip(), ln=True)
                    current_font_size = 12
                elif line.strip().startswith('- ') or line.strip().startswith('* '):
                    # List items - using a hyphen instead of bullet point
                    pdf.set_font('Arial', '', current_font_size)
                    item_text = line.strip()[2:].strip()
                    pdf.cell(10, 7, '-', 0, 0)  # Use hyphen instead of bullet point
                    pdf.multi_cell(0, 7, item_text)
                    in_list = True
                elif line.strip().startswith('---'):
                    pdf.ln(2)
                    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
                    pdf.ln(5)
                elif line.strip() == '':
                    # Empty line
                    pdf.ln(5)
                    in_list = False
                else:
                    # Regular text
                    if in_list and line.strip() and (line[0] == ' ' or line[0] == '\t'):
                        # Continuation of list item with indentation
                        pdf.set_font('Arial', '', current_font_size)
                        pdf.set_x(pdf.get_x() + 10)
                        pdf.multi_cell(0, 7, line.strip())
                    else:
                        in_list = False
                        # Handle bold text (very simplified approach)
                        if '**' in line:
                            parts = line.split('**')
                            for i, part in enumerate(parts):
                                if i % 2 == 0:  # Even parts are regular text
                                    pdf.set_font('Arial', '', current_font_size)
                                    pdf.write(7, part)
                                else:  # Odd parts are bold
                                    pdf.set_font('Arial', 'B', current_font_size)
                                    pdf.write(7, part)
                            pdf.ln()
                        else:
                            pdf.set_font('Arial', '', current_font_size)
                            pdf.multi_cell(0, 7, line)
            
            pdf.output(filename)
            return f"Report successfully exported to {filename}"
        except ImportError:
            return "Error: FPDF library not found. Install it with 'pip install fpdf2'"
        except Exception as e:
            return f"Error in PDF generation: {e}"