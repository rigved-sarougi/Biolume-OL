import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

# Set up environment for Jinja2 to load templates
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load offer letter template
template = env.get_template('offer_letter_template.txt')

# Streamlit App Title
st.title("Offer Letter Generator")

# Upload company logo
logo = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
if logo is not None:
    st.image(logo, caption="Uploaded Company Logo", use_column_width=True)

# Streamlit form for input
with st.form("offer_letter_form"):
    company_name = st.text_input("Company Name", value="Biolume Skin Science Pvt. Ltd.")
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")

    # Submit button
    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    # Employee data to fill in the template
    employee_data = {
        "company_name": company_name,
        "name": name,
        "designation": designation,
        "salary": salary,
        "joining_date": joining_date.strftime("%B %d, %Y")
    }

    # Render the offer letter content
    offer_letter_content = template.render(employee_data)

    # Display offer letter preview
    st.subheader("Preview Offer Letter:")
    st.text(offer_letter_content)

    # Option to download as PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Add the company logo to the PDF (optional)
    if logo is not None:
        pdf.image(logo, 10, 8, 33)
    
    pdf.set_font('Arial', '', 12)
    pdf.ln(20)  # Adding some space after the logo
    pdf.multi_cell(0, 10, offer_letter_content)

    # Save the PDF in memory
    pdf_output = f"Offer_Letter_{name}.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Download Offer Letter as PDF",
            data=pdf_file,
            file_name=pdf_output,
            mime='application/octet-stream'
        )

    # Optionally, remove the file after serving it
    if os.path.exists(pdf_output):
        os.remove(pdf_output)
