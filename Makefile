# Makefile for exporting the notebook to PDF with rendered markdown and charts

# Export notebook to PDF using nbconvert (renders markdown and charts)
export-pdf:
	jupyter nbconvert --to pdf stock_analysis.ipynb --output stock_analysis_report.pdf

# Clean generated PDF
clean:
	rm -f stock_analysis_report.pdf
