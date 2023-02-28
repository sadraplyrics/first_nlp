from pdf2image import convert_from_path
import pytesseract
texts_path = "/home/sadraplyrics/Desktop/Programming/DataScieince/python/data_science/nlp_paper/texts/"
def custom_convert_function(_filename: str):
    conv = ""
    pages = convert_from_path(f"{texts_path}{_filename}.pdf", 500)
    page_num = 0
    for page in pages:
        page.save(f"{texts_path}{_filename}{page_num}.jpg", "JPEG")
        conv += pytesseract.image_to_string(f"{texts_path}{_filename}{page_num}.jpg")
        page_num+=1
    with open(f"{texts_path}{_filename}.txt", "w+") as new_file:
            new_file.write(conv)

if __name__ == "__main__":
    print("TESTING MODE")

