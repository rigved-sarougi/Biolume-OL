import streamlit as st
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load the Jinja2 template
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template('offer_letter_template.txt')

st.title("Offer Letter Generator")

logo = 'Untitled design.png'  # Logo file path
background_image = 'ddd.png'  # Background image for A4

# Form for input
with st.form("offer_letter_form"):
    name = st.text_input("Employee Name")
    designation = st.text_input("Employee Designation")
    salary = st.text_input("Employee Salary (in Rs.)")
    joining_date = st.date_input("Joining Date")
    email = st.text_input("Employee Email")  # New field for email

    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    # Prepare employee data for the template
    employee_data = {
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
            if os.path.exists(logo):
                self.image(logo, x=85, y=10, w=40)  # Center the logo
            self.ln(20)  # Space after header

        def offer_letter_body(self, body):
            self.set_xy(20, 50)  # Set position for text
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

    # Create PDF
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.offer_letter_body(offer_letter_content)

    pdf_output = f"Offer_Letter_{name}.pdf"
    pdf.output(pdf_output)

    # Download PDF Button
    with open(pdf_output, "rb") as pdf_file:
        st.download_button(
            label="Download Offer Letter as PDF",
            data=pdf_file,
            file_name=pdf_output,
            mime='application/octet-stream'
        )

    # Email sending function
    def send_email(to_email, subject, body, attachment_file):
        from_email = "dataanalyst@biolume.in"  # Your email address
        password = "bio666666@"  # Use your App Password here

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
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(from_email, password)
                server.send_message(msg)
                return True
        except smtplib.SMTPAuthenticationError:
            return False, "SMTP Authentication Error: Check your email and password."
        except smtplib.SMTPConnectError:
            return False, "SMTP Connection Error: Unable to connect to the SMTP server."
        except Exception as e:
            return False, str(e)

    # Send email button
    if st.button("Send Offer Letter via Email"):
        if email:  # Check if email is provided
            email_result = send_email(
                to_email=email,
                subject=f"Offer Letter for {name}",
                body=offer_letter_content,
                attachment_file=pdf_output
            )
            if email_result is True:
                st.success("Email sent successfully!")
            else:
                st.error(f"Failed to send email: {email_result}")
        else:
            st.error("Please provide a valid email address.")

    # Clean up the generated PDF file
    if os.path.exists(pdf_output):
        os.remove(pdf_output)
