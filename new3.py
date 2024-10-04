import pandas as pd
import json
import matplotlib.pyplot as plt
from fpdf import FPDF

# Load the JSON data from the files
with open("/mnt/data/result.json", "r") as result_file:
    result_data = json.load(result_file)

with open("/mnt/data/SRE CHAOS SUMMARY REPORT.json", "r") as sre_file:
    sre_data = json.load(sre_file)

# Create a dataframe for result.json data
result_df = pd.DataFrame(result_data)

# Create a dataframe for SRE CHAOS SUMMARY REPORT.json data
sre_df = pd.DataFrame(sre_data)

# Generate Pie Chart from the 'Results' field in result.json
result_counts = result_df['Results'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Result Distribution in Experiments')
plt.savefig('/mnt/data/pie_chart.png')
plt.close()

# Generate PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Chaos Experiment and SRE Summary Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, dataframe, title):
        self.chapter_title(title)
        self.set_font('Arial', '', 10)
        for i in range(len(dataframe)):
            row = dataframe.iloc[i]
            line = ' | '.join([str(x) for x in row])
            self.multi_cell(0, 10, line)
        self.ln()

# Create PDF
pdf = PDF()

# Add Page and Report Title
pdf.add_page()
pdf.chapter_title("1. Chaos Experiment Results")

# Add Chaos Experiment Data Table from result.json
pdf.add_table(result_df, "Chaos Experiment Data Table")

# Add SRE Summary Report Data Table
pdf.add_page()
pdf.chapter_title("2. SRE Summary Report")
pdf.add_table(sre_df, "SRE Summary Data Table")

# Add Pie Chart
pdf.add_page()
pdf.chapter_title("3. Result Distribution Pie Chart")
pdf.image('/mnt/data/pie_chart.png', x=10, y=40, w=190)

# Save the PDF
pdf_output_path = '/mnt/data/Chaos_SRE_Report.pdf'
pdf.output(pdf_output_path)

print(f"PDF report saved as {pdf_output_path}")

