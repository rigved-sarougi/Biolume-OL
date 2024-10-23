import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Define the directory where the offer letter template is stored
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Load the offer letter template
template = env.get_template('offer_letter_template.txt')

# Streamlit app title
st.title("Offer Letter Generator")

# Logo image path and background image path
logo = 'Untitled design.png'
background_image = 'ddd.png'  # Path to the background image

# Form to collect user input
with st.form("offer_letter_form"):
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")
    email = st.text_input("Recipient Email")  # Input for recipient email

    # Button to submit the form
    submitted = st.form_submit_button("Generate Offer Letter")

# If the form is submitted
if submitted:
    # Prepare the data for rendering the template
    employee_data = {
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
            # Add background image for the entire page
            if os.path.exists(background_image):
                self.image(background_image, x=0, y=0, w=210, h=297)  # A4 size dimensions

            # Place the logo at the top middle of the page, smaller size
            if os.path.exists(logo):
                page_width = self.w  # Get page width
                logo_width = 40  # Smaller width for the logo
                x_position = (page_width - logo_width) / 2  # Calculate center
                self.image(logo, x=x_position, y=15, w=logo_width)  # y=15 for top margin

            self.ln(30)  # Adjust the space after the logo

        def offer_letter_body(self, body):
            # Set margins and font for content
            self.set_left_margin(20)
            self.set_right_margin(20)
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 8, body)

        def footer(self):
            # Add footer information (page number)
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

    # Function to send email with attachment
    def send_email(to_email, subject, body, attachment_file):
        from_email = "dataanalyst@biolume.in"  # Your email address
        password = "bio666666@"  # Your email password (or app-specific password)

        # Create a multipart email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))

        # Attach the PDF file
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_file)}')
            msg.attach(part)

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Update to your SMTP server
                server.starttls()  # Upgrade to secure connection
                server.login(from_email, password)
                server.send_message(msg)
            return True
        except Exception as e:
            return False, str(e)

    # Send email with the offer letter
    email_subject = f"Offer Letter for {name}"
    email_body = f"Dear {name},\n\nPlease find attached your offer letter.\n\nBest Regards,\nBiolume Skin Science Pvt. Ltd."
    
    if email:
        result = send_email(email, email_subject, email_body, pdf_output)
        if result is True:
            st.success(f"Offer letter sent successfully to {email}!")
        else:
            st.error(f"Failed to send email: {result[1]}")

    # Remove the generated PDF file after downloading
    if os.path.exists(pdf_output):
        os.remove(pdf_output)
