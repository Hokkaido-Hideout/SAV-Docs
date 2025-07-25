# How to Use It:
# python generate_search_index.py README.md search-index.json

import markdown2
from bs4 import BeautifulSoup
import json
import re
import sys
import os

def generate_search_index(md_path, output_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown2.markdown(md_text, extras=["fenced-code-blocks", "header-ids"])
    soup = BeautifulSoup(html, "html.parser")

    sections = []
    current_section = {"id": "", "title": "", "body": ""}

    for element in soup.find_all(["h2", "h3", "h4", "p", "pre", "ul", "ol", "blockquote", "div"]):
        if element.name in ["h2"]:
            if current_section["title"]:
                sections.append(current_section)
            section_id = re.sub(r'\W+', '-', element.get_text().lower()).strip("-")
            current_section = {
                "id": section_id,
                "title": element.get_text(),
                "body": ""
            }
        else:
            current_section["body"] += element.get_text(separator=" ", strip=True) + " "

    if current_section["title"]:
        sections.append(current_section)

    for section in sections:
        section["body"] = section["body"].strip()[:1000]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_search_index.py <README.md path> <output JSON path>")
    else:
        md_file = sys.argv[1]
        json_file = sys.argv[2]
        generate_search_index(md_file, json_file)
        print(f"Generated search index at: {json_file}")
