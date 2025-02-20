import pandas as pd
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML

# Load data
df = pd.read_excel("granttracking.xlsx")
page_list = df["Website Link"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for page in page_list:
    response = requests.get(page, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        html_content = str(soup)  # Convert to string before saving

        # Ensure Grant Name is properly retrieved
        grant_name = df.loc[df["Website Link"] == page, "Grant Name"]
        if not grant_name.empty:
            grant_name = grant_name.iloc[0]  # Extract string value
        else:
            grant_name = "Unknown_Grant"

        # Save HTML content to a file
        html_filename = f"{grant_name}.html"
        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Convert saved HTML to PDF
        pdf_filename = f"{grant_name}.pdf"
        HTML(string=html_content).write_pdf(pdf_filename)

        print(f"Saved: {pdf_filename}")
    else:
        print(f"Failed to fetch {page}")
