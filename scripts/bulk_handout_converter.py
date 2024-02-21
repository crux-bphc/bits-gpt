from typing import Any
import os
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import tabula
import pandas as pd
import pdf_to_txt

'''This script is to extract the raw tables and raw texts from PDF handouts'''


def handout_convert(path): #extracts only texts from the pdfs
    basename = os.path.splitext(os.path.basename(path))[0]
    basename = basename.replace(" ","_")
    print("converting", basename)
    raw_pdf_elements = partition_pdf(
        filename=path,
        # Unstructured first finds embedded image blocks
        extract_images_in_pdf=False,
        strategy="hi_res",
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

    class Element(BaseModel):
        type: str
        text: Any

    # Categorize by type
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    # Text
    text_elements = [e for e in categorized_elements if e.type == "text"]
    texts = [i.text for i in text_elements]

    # Write to disk   
    for i in range(0, len(texts)):
        with open(f"data/Handouts/rawdata/rawtext_{basename}_{i:04d}.txt", "w", encoding="utf-8") as handle:
            handle.write(texts[i])


def extract_tables_batch(handout_path, output_path): #extracts only tables from the pdfs in csv format
    tabula.convert_into_by_batch(handout_path, output_format="csv", pages="all", java_options="-Dfile.encoding=UTF8")
    file_list = os.listdir(handout_path)
    #find all csv files and move them to the output_path, also replaces whitespaces with _ and adds the prefix "rawtable_" to the filename
    for file in file_list:
        if file.endswith(".csv"):
            os.rename(os.path.join(handout_path, file), os.path.join(output_path, "rawtable_"+file.replace(" ","_")))

def extract_texts(path):
    filelist = os.listdir(path)
    for handout in filelist:
        handout = os.path.join(path, handout)
        if os.path.isfile(handout):
            handout_convert(handout)
            

def main():
    extract_texts("data\\Handouts")
    extract_tables_batch("data\\Handouts", "data\\Handouts\\rawdata")

if __name__ == "__main__":
    main()
