import requests
from bs4 import BeautifulSoup
import pdfkit

# Base URL (modify as needed)
base_url = "https://iratracker.org/actions/?fwp_paged="

# Set headers to mimic a browser request (optional)
headers = {
    "User-Agent": "Mozilla/5.0"
}
print("orange")


# Loop through multiple pages (adjust range as needed)
for page in range(1, 61):  # Change range to match total number of pages
    url = f"{base_url}{page}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Save the HTML content
        html_filename = f"page_{page}.html"
        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(str(soup))

        # Convert the saved HTML to PDF
        
        pdf_filename = f"page_{page}.pdf"
        config = pdfkit.configuration(wkhtmltopdf='/path/to/wkhtmltopdf')
        pdfkit.from_file(html_filename, pdf_filename, configuration=config)


        print(f"Saved: {pdf_filename}")
    else:
        print(f"Failed to fetch {url}")
