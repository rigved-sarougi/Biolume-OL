import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

template = env.get_template('offer_letter_template.txt')

st.title("Offer Letter Generator")

logo = 'Untitled design.png'

with st.form("offer_letter_form"):
    company_name = "Biolume Skin Science Pvt. Ltd."
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")

    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    employee_data = {
        "company_name": company_name,
        "name": name,
        "designation": designation,
        "salary": salary,
        "joining_date": joining_date.strftime("%B %d, %Y")
    }

    offer_letter_content = template.render(employee_data)

    st.subheader("Preview Offer Letter:")
    st.text(offer_letter_content)

    class PDF(FPDF):
        def header(self):
            if os.path.exists('Black & Orange Professional Company Letter A4 Document.png'):
                self.image('Black & Orange Professional Company Letter A4 Document.png', x=0, y=0, w=210, h=297)
            if logo is not None:
                self.image(logo, 10, 8, 33)

        def offer_letter_body(self, body):
            margin_left = 20
            margin_top = 50
            self.set_xy(margin_left, margin_top)
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.offer_letter_body(offer_letter_content)

    pdf_output = f"Offer_Letter_{name}.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Download Offer Letter as PDF",
            data=pdf_file,
            file_name=pdf_output,
            mime='application/octet-stream'
        )

    if os.path.exists(pdf_output):
        os.remove(pdf_output)
