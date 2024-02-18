from typing import Any
import os
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf

'''This script is to extract the raw tables and raw texts from PDF handouts'''


def handout_convert(path):
    basename = os.path.splitext(os.path.basename(path))[0]
    basename = basename.replace(" ","_")
    print("converting", basename)
    raw_pdf_elements = partition_pdf(
        filename=path,
        # Unstructured first finds embedded image blocks
        extract_images_in_pdf=False,
        # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
        # Titles are any sub-section of the document
        infer_table_structure=True,
        # Post processing to aggregate text once we have the title
        chunking_strategy="by_title",
        # Chunking params to aggregate text blocks
        # Attempt to create a new chunk 3800 chars
        # Attempt to keep chunks > 2000 chars
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
    )

    # Create a dictionary to store counts of each type
    category_counts = {}

    for element in raw_pdf_elements:
        category = str(type(element))
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    # Unique_categories will have unique elements
    unique_categories = set(category_counts.keys())
    print(category_counts)

    class Element(BaseModel):
        type: str
        text: Any


    # Categorize by type
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    # Tables
    table_elements = [e for e in categorized_elements if e.type == "table"]
    tables = [i.text for i in table_elements]

    # Text
    text_elements = [e for e in categorized_elements if e.type == "text"]
    texts = [i.text for i in text_elements]

    for i in range(0, len(tables)):
        with open(f"data/Handouts/rawdata/rawtable_{basename}_{i:04d}.txt", "w", encoding="utf-8") as handle:
            handle.write(tables[i])
    
    for i in range(0, len(texts)):
        with open(f"data/Handouts/rawdata/rawtext_{basename}_{i:04d}.txt", "w", encoding="utf-8") as handle:
            handle.write(texts[i])

def parse_all_handouts(path):
    filelist = os.listdir(path)
    for handout in filelist:
        handout = os.path.join(path, handout)
        if os.path.isfile(handout):
            handout_convert(handout)

def main():
    parse_all_handouts("data\\Handouts")

if __name__ == "__main__":
    main()
