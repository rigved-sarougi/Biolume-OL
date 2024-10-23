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

# Logo image path
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
            # Add header background image (A4 size)
            if os.path.exists('Black & Orange Professional Company Letter A4 Document.png'):
                self.image('Black & Orange Professional Company Letter A4 Document.png', x=0, y=0, w=210, h=297)
            # Add company logo to the header
            if logo is not None:
                self.image(logo, 10, 8, 33)

        def offer_letter_body(self, body):
            # Set margins for A4 format (standard A4 width = 210mm, height = 297mm)
            margin_left = 20
            margin_top = 60
            self.set_xy(margin_left, margin_top)
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

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
