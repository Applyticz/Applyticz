from bs4 import BeautifulSoup
import re

def extract_plain_text(html_body):
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(html_body, "html.parser")

    # Extract the plain text from the HTML
    plain_text = soup.get_text(separator=" ").strip()  # Adding space between elements

    # Replace unwanted escape sequences like \r\n with a single space or appropriate separator
    plain_text = re.sub(r'\s+', ' ', plain_text)  # Replace multiple whitespace characters with a single space

    return plain_text

