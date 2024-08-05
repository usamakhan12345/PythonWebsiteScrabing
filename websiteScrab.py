# import requests
# from bs4 import BeautifulSoup

# def scrape_page(url):
#     # Send an HTTP request to the URL
#     response = requests.get(url)
#     if response.status_code != 200:
#         print(f"Failed to retrieve {url}")
#         return None
    
#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Extract and print all the headings (h1, h2, etc.)
#     headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
#     print(f"\nHeadings from {url}:")
#     for heading in headings:
#         print(heading.text.strip())

#     # Extract and print all the paragraphs
#     paragraphs = soup.find_all('p')
#     print(f"\nParagraphs from {url}:")
#     for paragraph in paragraphs:
#         print(paragraph.text.strip())

#     return soup

# # Main URL to scrape
# main_url = 'https://fuuast.edu.pk/faculty-of-science-technology/'

# # Scrape the main page
# main_soup = scrape_page(main_url)

# # Extract all the links
# if main_soup:
#     links = main_soup.find_all('a')
#     print("\nLinks found on the main page:")
#     for link in links:
#         href = link.get('href')
#         if href and href.startswith('http'):
#             print(href, link.text.strip())
#             # Scrape each link
#             scrape_page(href)






import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='scraping.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scraped Content', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()

def scrape_page(url, pdf):
    print(f"Scraping URL: {url}")
    try:
        # Send an HTTP request to the URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve {url}: {e}")
        print(f"Failed to retrieve {url}: {e}")
        return None

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Add the URL as a chapter title in the PDF
    pdf.add_page()
    pdf.chapter_title(f"Content from {url}")

    # Extract and add all the headings (h1, h2, etc.) to the PDF
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6' , 'p'])
    headings_text = "\n".join(heading.text.strip() for heading in headings)
    pdf.chapter_body(headings_text)

    # Extract and add all the paragraphs to the PDF 
    paragraphs = soup.find_all('p')
    paragraphs_text = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
    pdf.chapter_body(paragraphs_text)

    return soup

# Main URL to scrape
main_url = 'https://fuuast.edu.pk/students/'

# Create a PDF document
pdf = PDF()
pdf.set_left_margin(10)
pdf.set_right_margin(10)

# Scrape the main page
main_soup = scrape_page(main_url, pdf)

# Extract all the links and scrape each link
if main_soup:
    links = main_soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.startswith('http'):
            scrape_page(href, pdf)

# Save the PDF to a file
print("Saving PDF file...")
pdf.output('scraped_content_about-student_Des.pdf')
print("PDF file saved as 'scraped_content.pdf'")


