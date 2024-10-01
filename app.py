import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

# Set up environment for Jinja2 to load templates
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load offer letter template
template = env.get_template('offer_letter_template.txt')

# Set up page title and favicon
st.set_page_config(
    page_title="Offer Letter Generator",
    page_icon=":memo:",
    layout="wide"
)

# Streamlit App Title and Description
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Offer Letter Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Easily generate professional offer letters with your company's branding.</p>", unsafe_allow_html=True)

# Upload company logo
st.sidebar.markdown("<h2 style='text-align: center;'>Upload Company Logo</h2>", unsafe_allow_html=True)
logo = st.sidebar.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])

if logo:
    st.sidebar.image(logo, caption="Company Logo Preview", use_column_width=True)

# Streamlit form for input
with st.form("offer_letter_form"):
    st.markdown("<h3>Company Details</h3>", unsafe_allow_html=True)
    company_name = st.text_input("Company Name", value="Biolume Skin Science Pvt. Ltd.")

    st.markdown("<h3>Employee Details</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Employee Name")
        salary = st.text_input("Employee Salary (in Rs.)")

    with col2:
        designation = st.text_input("Employee Designation")
        joining_date = st.date_input("Joining Date")

    # Submit button
    submitted = st.form_submit_button("Generate Offer Letter")

# Generate offer letter if form is submitted
if submitted:
    if not name or not designation or not salary or not company_name:
        st.error("Please fill out all the fields before generating the offer letter.")
    else:
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

        # Display offer letter preview in a styled container
        st.markdown("<h3>Offer Letter Preview</h3>", unsafe_allow_html=True)
        st.text_area("Preview", value=offer_letter_content, height=300)

        # Generate the PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add the company logo to the PDF if uploaded
        if logo:
            logo_path = f"temp_logo_{name}.png"
            with open(logo_path, "wb") as f:
                f.write(logo.getbuffer())
            pdf.image(logo_path, 10, 8, 33)
            os.remove(logo_path)  # Clean up the temporary logo file

        pdf.set_font('Arial', 'B', 12)
        pdf.ln(20)  # Space after the logo
        pdf.multi_cell(0, 10, offer_letter_content)

        # Save the PDF in memory
        pdf_output = f"Offer_Letter_{name}.pdf"
        pdf.output(pdf_output)

        # Download button for the generated PDF
        with open(pdf_output, "rb") as pdf_file:
            st.download_button(
                label="Download Offer Letter as PDF",
                data=pdf_file,
                file_name=pdf_output,
                mime='application/pdf'
            )

        # Remove the generated PDF after serving it
        if os.path.exists(pdf_output):
            os.remove(pdf_output)

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        Developed by Biolume Skin Science Pvt. Ltd.
    </div>
    """,
    unsafe_allow_html=True
)
