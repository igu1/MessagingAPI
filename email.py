import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader # type: ignore
from .exception import EmailException
import re

class Email:
    """
    A class for sending emails using SMTP protocol with support for HTML templates.

    This class provides functionality to send emails using SMTP servers (default: Gmail),
    with support for both plain text and HTML template-based emails using Jinja2.

    Args:
        from_email (str): The sender's email address
        app_password (str): The application password for authentication
        host (str, optional): SMTP server host. Defaults to 'smtp.gmail.com'
        port (int, optional): SMTP server port. Defaults to 587
        templates_dir (str, optional): Directory path containing email templates. Defaults to None

    Attributes:
        password (str): The stored application password
        from_email (str): The sender's email address
        host (str): SMTP server host
        port (int): SMTP server port
        env (Environment): Jinja2 environment for template rendering
    """
    
    def __init__(self, from_email, app_password, host='smtp.gmail.com', port=587, templates_dir=None):
        self.password = app_password
        self.from_email = from_email
        self.host = host
        self.port = port
        self.env = None
        if templates_dir:
            self.env = Environment(loader=FileSystemLoader(templates_dir))
    
    
    def __str__(self):
        """Returns a string representation of the Email object."""
        return f"Email (from_email={self.from_email}, host={self.host}, port={self.port})"
    
    def init_env(self, templates_dir):
        """
        Initialize the Jinja2 environment with the specified templates directory.

        Args:
            templates_dir (str): Path to the directory containing email templates
        """
        self.env = Environment(loader=FileSystemLoader(templates_dir))
    
    def _get_template(self, template, context=None):
        """
        Get and render a template with the given context.

        Args:
            template (str): Name of the template file
            context (dict, optional): Dictionary of variables to pass to the template. Defaults to None

        Returns:
            str: The rendered template content

        Raises:
            EmailException: If the environment is not initialized
        """
        if not self.env:
            raise EmailException("Environment not initialized. Call Email.init_env() first.")
        template = self.env.get_template(template)
        return template.render(context or {})
    
    def _validate_email(self, email):
        """
        Validate an email address using regex.

        Args:
            email (str): Email address to validate

        Raises:
            EmailException: If the email address is invalid
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise EmailException(f"Invalid email address. Please provide a valid email address.") 
    
    def send(self, to_email=None, body=None, template=None, context=None):
        """
        Send an email to one or multiple recipients.

        Args:
            to_email (str or list): Single email address or list of email addresses
            body (str, optional): Plain text email content. Used if template is None
            template (str, optional): Name of the template file to use
            context (dict, optional): Dictionary of variables to pass to the template

        Raises:
            EmailException: If recipient email is not provided or if email validation fails
        """
        if not to_email:
            raise EmailException("Recipient email(s) must be provided.")
    
        to_email = [str(email) for email in (to_email if isinstance(to_email, list) else [to_email])]      
        
        for email in to_email:
            self._validate_email(email)
            
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ', '.join(to_email) 
        
        if template:
            template_content = self._get_template(template=template, context=context)
            msg.attach(MIMEText(template_content, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(self.host, self.port)
        server.starttls()
        server.login(self.from_email, self.password)
        server.send_message(msg)
        server.quit()