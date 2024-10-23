import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

# Define the directory where the offer letter template is stored
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load the offer letter template
template = env.get_template('offer_letter_template.txt')

# Streamlit app title
st.title("Offer Letter Generator")

# Logo image path - ensure the logo is in the same directory as the script
logo = 'Untitled design.png'

# Form to collect user input
with st.form("offer_letter_form"):
    company_name = "Biolume Skin Science Pvt. Ltd."
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")

    # Button to submit the form
    submitted = st.form_submit_button("Generate Offer Letter")

# If the form is submitted
if submitted:
    # Prepare the data for rendering the template
    employee_data = {
        "company_name": company_name,
        "name": name,
        "designation": designation,
        "salary": salary,
        "joining_date": joining_date.strftime("%B %d, %Y")
    }

    # Render the offer letter content using the Jinja2 template
    offer_letter_content = template.render(employee_data)

    # Display a preview of the offer letter
    st.subheader("Preview Offer Letter:")
    st.text(offer_letter_content)

    # Define a custom PDF class to create the offer letter in A4 size
    class PDF(FPDF):
        def header(self):
            # Set the header with text instead of an image
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Biolume Skin Science Pvt. Ltd.', ln=True, align='C')
            self.cell(0, 10, 'Ground Floor, Rampal Awana Complex', ln=True, align='C')
            self.cell(0, 10, 'Rampal Awana Complex, Indra Market', ln=True, align='C')
            self.cell(0, 10, 'Sector-27, Atta, Gautambuddha Nagar, Noida Uttar Pradesh 201301', ln=True, align='C')
            self.ln(20)  # Adds space after the header
            
            # Insert logo at the top-left corner
            if os.path.exists(logo):
                self.image(logo, 10, 8, 33)  # Adjust these values if the logo is not appearing

        def offer_letter_body(self, body):
            # Set margins for A4 format (standard A4 width = 210mm, height = 297mm)
            margin_left = 20
            margin_top = 60
            self.set_xy(margin_left, margin_top)
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

        def footer(self):
            # Add footer information (page number or additional details if needed)
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    # Create a PDF document in A4 format
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Add the offer letter content to the PDF
    pdf.offer_letter_body(offer_letter_content)

    # Define the output PDF file name
    pdf_output = f"Offer_Letter_{name}.pdf"
    pdf.output(pdf_output)

    # Allow the user to download the PDF via a download button
    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Download Offer Letter as PDF",
            data=pdf_file,
            file_name=pdf_output,
            mime='application/octet-stream'
        )

    # Remove the generated PDF file after downloading
    if os.path.exists(pdf_output):
        os.remove(pdf_output)
