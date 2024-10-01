import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

# Set up environment for Jinja2 to load templates
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load offer letter template
template = env.get_template('offer_letter_template.txt')

# Custom CSS for professional styling
st.markdown("""
    <style>
    /* Custom fonts from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
    }

    h1 {
        color: #333333;
        text-align: center;
        padding: 10px;
    }

    .stApp {
        background-color: #f4f4f4;
        padding: 20px;
    }

    .main-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    .company-info {
        text-align: center;
        font-size: 1.2em;
        font-weight: 500;
        color: #4CAF50;
        margin-bottom: 40px;
    }

    .stTextInput > div {
        padding-bottom: 15px;
    }

    .stDownloadButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stDownloadButton > button:hover {
        background-color: #45A049;
    }

    textarea {
        font-size: 1.1em;
        line-height: 1.6;
    }

    footer {
        text-align: center;
        font-size: 0.8em;
        color: #666;
        padding: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Set up page title and favicon
st.set_page_config(
    page_title="Offer Letter Generator",
    page_icon=":briefcase:",
    layout="wide"
)

# Streamlit App Title and Description
st.markdown("<h1>Professional Offer Letter Generator</h1>", unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Company Name and Logo Section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Upload company logo
        logo = st.file_uploader("Upload Company Logo", type=["png", "jpg", "jpeg"])
        if logo:
            st.image(logo, caption="Company Logo", use_column_width=True)

    with col2:
        # Company Name Input
        company_name = st.text_input("Company Name", value="Biolume Skin Science Pvt. Ltd.")
    
    st.markdown("<div class='company-info'>" + company_name + "</div>", unsafe_allow_html=True)

    # Employee and Offer Details Section
    st.markdown("<h3>Employee Details</h3>", unsafe_allow_html=True)
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")

    # Submit button
    generate_button = st.button("Generate Offer Letter")

    if generate_button and name and designation and salary and joining_date:
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

        # Display offer letter preview in a styled textarea
        st.markdown("<h3>Offer Letter Preview</h3>", unsafe_allow_html=True)
        st.text_area("", value=offer_letter_content, height=300)

        # Option to download as PDF
        pdf = FPDF()
        pdf.add_page()

        # Add the company logo to the PDF if uploaded
        if logo:
            logo_path = f"temp_logo_{name}.png"
            with open(logo_path, "wb") as f:
                f.write(logo.getbuffer())
            pdf.image(logo_path, 10, 8, 33)
            os.remove(logo_path)  # Clean up the temporary logo file

        pdf.set_font('Arial', '', 12)
        pdf.ln(20)  # Space after the logo
        pdf.multi_cell(0, 10, offer_letter_content)

        # Save the PDF in memory
        pdf_output = f"Offer_Letter_{name}.pdf"
        pdf.output(pdf_output)

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

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer>
    Developed by Biolume Skin Science Pvt. Ltd.
    </footer>
    """,
    unsafe_allow_html=True
)
