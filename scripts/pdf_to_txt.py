import os
import fitz


def convert_pdf_to_text(pdf_path, output_path):
    try:
        with fitz.open(pdf_path) as pdf_document:
            text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()

            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)

        print(f"Conversion successful: {pdf_path}")
    except Exception as e:
        print(f"Conversion failed for {pdf_path}. Error: {e}")


def convert_pdfs_in_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, os.path.splitext(filename)[0] + ".txt"
            )
            convert_pdf_to_text(pdf_path, output_path)


if __name__ == "__main__":
    input_directory = "./data"
    output_directory = "./data"
    print(f"Converting PDFs from {input_directory} to {output_directory}")
    convert_pdfs_in_directory(input_directory, output_directory)
