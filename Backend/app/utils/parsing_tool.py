from bs4 import BeautifulSoup

def extract_plain_text(html_body):
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(html_body, "html.parser")

    # Extract the plain text from the HTML
    plain_text = soup.get_text(separator="\n").strip()

    return plain_text

