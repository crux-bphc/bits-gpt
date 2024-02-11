import tabula
import pandas as pd
import os
import pdf_to_txt

handout_path = "data\\Handouts"
output_path = "data\\Handouts\\CSV"

def extract_tables():
    file_list = os.listdir(handout_path)
    for file_name in file_list:
        file_path = os.path.join(handout_path, file_name)
        if os.path.isfile(file_path):
            df_list = tabula.read_pdf(file_path, pages="all",pandas_options={'header': None})
            count = 1
            for df in df_list:
                df.to_csv(os.path.join(output_path, os.path.splitext(file_name)[0])+str(count)+".csv")
                count+=1

def extract_all_text():
    pdf_to_txt.convert_pdfs_in_directory("data\\Handouts", "data\\Handouts\\CSV")
    #figure out a way to extract only non-tabular data from the pdfs

#extract_all_text()
extract_tables()