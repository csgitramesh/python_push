import pandas as pd
import json
from fpdf import FPDF

# Load the JSON data from the files
with open("/home/ec2-user/python/result.json", "r") as result_file:
    result_data = json.load(result_file)

with open("/home/ec2-user/python/SRE CHAOS SUMMARY REPORT.json", "r") as sre_file:
    sre_data = json.load(sre_file)

# Create a dataframe for result.json data
result_df = pd.DataFrame(result_data)

# Create a dataframe for SRE CHAOS SUMMARY REPORT.json data
sre_df = pd.DataFrame(sre_data)

# Generate PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SRE CHAOS SUMMARY REPORT', 0, 1, 'C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(50, 10, title, 0, 0)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, content, 0, 1)
        self.ln(4)

    def add_results_section(self, dataframe):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chaos Test Results:', 0, 1)
        self.ln(4)
        
        self.set_font('Arial', '', 12)
        for i in range(len(dataframe)):
            row = dataframe.iloc[i]
            # Print each experiment in a simple format
            experiment_text = f"Experiment: {row['Experiment']} | Results: {row['Results']}"
            self.multi_cell(0, 10, experiment_text)
            self.ln(2)

# Create PDF
pdf = PDF()

# Add Page and Report Title
pdf.add_page()

# Add the SRE Chaos Summary Report sections
pdf.add_section("Application Name", sre_df.loc[0, "Details"])
pdf.add_section("Services in Scope", sre_df.loc[1, "Details"])
pdf.add_section("Application Members Participated", sre_df.loc[2, "Details"])
pdf.add_section("SRE Members Participated", sre_df.loc[3, "Details"])
pdf.add_section("Chaos Test Execution Date", sre_df.loc[4, "Details"])
pdf.add_section("Chaos Tool Used", sre_df.loc[5, "Details"])
pdf.add_section("Disposition", sre_df.loc[6, "Details"])
pdf.add_section("Environment", sre_df.loc[7, "Details"])

# Add Results Section from result.json
pdf.add_results_section(result_df)

# Save the PDF
pdf_output_path = '/home/ec2-user/python/Chaos_SRE_Report_Simple.pdf'
pdf.output(pdf_output_path)

print(f"PDF report saved as {pdf_output_path}")

