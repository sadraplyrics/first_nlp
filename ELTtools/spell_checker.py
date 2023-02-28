from string import punctuation
import docx
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
import unicodedata
from autocorrect import Speller
import sys
texts_path = "/home/sadraplyrics/Desktop/Programming/DataScieince/python/data_science/nlp_paper/texts/"
def remove_signs(text: str):
    punctuation = dict.fromkeys(i for i in range(sys.maxunicode)\
        if unicodedata.category(chr(i)).startswith("P"))
    return [string.translate(punctuation) for string in text]


def docx_spell_checker(_filename: str):
    mistakes = 0
    speller = SpellChecker()
    contents = ""
    doc = docx.Document(f"{texts_path}{_filename}.docx")
    for para in doc.paragraphs:
        contents += para.text + "\n"
    res = word_tokenize(contents)
    res = remove_signs(res)
    print(res)
    out = ""
    for word in res:
        corrected = speller.candidates(word)
        if word == " " or word == "":
            continue
        elif word != corrected:
            mistakes += 1
            out += f"{word} (Did you mean {corrected})\n"
            continue
        out += word + "\n"
    with open(f"{texts_path}{_filename}.txt", "w+") as new_file:
        new_file.write(out)


def txt_spell_checker(_filename):
    mistakes = 0
    speller = SpellChecker()
    with open(f"{texts_path}{_filename}.txt", "r") as new_file:
        contents = new_file.read()
    res = word_tokenize(contents)
    res = remove_signs(res)
    print(res)
    out = ""
    for word in res:
        corrected = speller.candidates(word)
        if word == " " or word == "":
            continue
        elif word != corrected:
            mistakes += 1
            out += f"{word} (Did you mean {corrected})\n"
            continue
        out += word + "\n"
    with open(f"{texts_path}{_filename}.txt", "w+") as new_file:
        new_file.write(out)
    

def simple_corrector(_filename):
    auto_speller = Speller()
    with open(f"{texts_path}{_filename}.txt") as new_file:
        contents = new_file.read()
    res = word_tokenize(contents)
    res = remove_signs(res)
    print(res)
    out = ""
    for word in res:
        out += auto_speller(word) + "\n"
    with open(f"{texts_path}{_filename}.txt", "w+") as new_file:
        new_file.write(out)

if __name__ == "__main__":
    simple_corrector("check")