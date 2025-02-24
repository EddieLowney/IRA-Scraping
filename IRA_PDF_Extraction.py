'''
Author: Eddie Lowney
Description: Scraping for IRA Grant PDFs to other format
Date:
Output:
'''
from collections import defaultdict, Counter
from pdfminer.high_level import extract_text
import os
import csv

class Textinator:
    def __init__(self):
        """ Constructor
        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_list = list()

    def load_text(self, filename, label=None, parser=None, GPT = False):
        results = parser(filename, GPT = False)


        if label is None:
            label = filename

    def pdf_parser(self, filename, GPT = False):
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_name = f'{base_name}.txt'

        text = extract_text(filename)
        with open(output_name, 'w') as file:
            file.write(text)

        # Gets word counts in a Counter datatype
# T = Textinator()
#
# T.load_text("/Users/eddielowney/Documents/IRA Tracking/rcpp-2024-awarded-projects.pdf",
#             'I1', parser=T.pdf_parser, GPT = False)

file_string = ""
with open("rcpp-2024-awarded-projects.txt", "r") as infile:
    lines = infile.readlines()
    for i in lines:
        file_string += i
file_list = file_string.split("\n\n")

recipient_separated_list = []
# for i in file_list:
#     i.replace("'", "")
print(file_list)
for i in range(len(file_list)):

    if "$" in file_list[i]:
        recipient_separated_list.append(file_list[(i-5):(i+1)])

for i in recipient_separated_list:
    print(i)
    print("orange")

output_file = "output.csv"

# Writing to CSV
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(recipient_separated_list)

print(f"CSV file saved as {output_file}")