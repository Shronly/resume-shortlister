import os
import fitz


def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF and extracts all text from every page.
    Returns one clean string of all text.
    """
    text = ""  #start with empty string,keep adding later

    doc = fitz.open(pdf_path)

    for page in doc: #iterate over all pages in resume
        text+= page.get_text() # extract text from this page and add to string

    #clean up the text - remove extra blank lines
    lines = text.splitlines() #split into individual lines
    cleaned_lines  = [line for line in lines if line.strip()]  # remove empty lines
    cleaned_text = "\n".join(cleaned_lines) #join back together 

    return cleaned_text.strip() #remove leading/trailing whitespace


# this block runs only when you run this file directly
if __name__ == "__main__":
    path = "uploads/resume.pdf"
    
    if not os.path.exists(path):
        print("ERROR: No resume found at", path)
    else:
        result = extract_text_from_pdf(path)
        print(result)
        print("\n--- Total characters extracted:", len(result))

    